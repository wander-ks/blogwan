from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article
from articles.serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleWriteSerializer
from articles.permissions import IsAuthorOrReadOnly
from articles.tasks import increase_views_async, invalidate_article_cache
from interactions.models import ArticleLike   # 点赞模型
from articles.tasks import send_new_article_notification
from points.services import update_points
from points.utils import generate_download_token
from notifications.models import Message
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt
from points.utils import consume_download_token
from articles.models import Article

@csrf_exempt
def download_file(request):
    token = request.GET.get('token')
    if not token:
        return HttpResponse('缺少下载凭证', status=400)
    article_id, user_id = consume_download_token(token)
    if not article_id:
        return HttpResponse('下载链接无效或已过期', status=404)
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return HttpResponse('文章不存在', status=404)

    # 准备文件内容
    file_content = (
        f"标题：{article.title}\n"
        f"作者：{article.author.username}\n"
        f"发布时间：{article.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        f"阅读量：{article.views}\n\n"
        f"正文：\n{article.content}"
    )
    safe_filename = escape_uri_path(f"{article.title}.txt")
    response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{safe_filename}"
    return response

class ArticleViewSet(viewsets.ModelViewSet):
    """
    文章视图集：提供 list, create, retrieve, update, destroy, like 操作
    """
    queryset = Article.objects.filter(is_published=True).select_related('author')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views', 'likes']
    ordering = ['-created_at']


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        article = self.get_object()
        user = request.user

        if user == article.author:
            return Response({'error': '不能下载自己的文章'}, status=400)

        user_points = user.points.balance
        if user_points < 1:
            return Response({'error': '积分不足，无法下载'}, status=400)

        # 扣除下载者积分，增加作者积分
        update_points(user, -1, 'download_pay', related_id=str(article.id), description=f'下载文章《{article.title}》')
        update_points(article.author, 1, 'download_income', related_id=str(article.id),
                      description=f'用户{user.username}下载您的文章')

        # 生成临时下载 token
        token = generate_download_token(article.id, user.id)
        download_url = f'/api/v1/articles/download-file/?token={token}'

        # 创建站内信，包含下载链接
        Message.objects.create(
            recipient=user,
            message_type='system',
            title=f'文章下载：《{article.title}》',
            content=f'您已成功支付 1 积分，点击下方链接下载文章（链接有效期 1 小时）。',
            link=download_url
        )

        return Response({'message': '下载请求已受理，请在收件箱中查看下载链接'})

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArticleWriteSerializer
        return ArticleDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        # 缓存处理
        user_id = request.user.id if request.user.is_authenticated else 0
        cache_key = f'article_detail_{kwargs["pk"]}_user_{user_id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, 300)  # 缓存5分钟
        # 异步增加阅读量
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        increase_views_async.delay(kwargs['pk'], ip)
        return response

    def perform_create(self, serializer):
        article = serializer.save(author=self.request.user)
        # 发布文章获得10积分
        update_points(self.request.user, 10, 'publish_article', related_id=str(article.id),description=f'发布文章《{article.title}》')
        # 异步通知粉丝
        send_new_article_notification.delay(article.id, article.author.id, article.title)


    def perform_update(self, serializer):
        instance = serializer.save()
        # 更新后清除旧缓存
        invalidate_article_cache.delay(instance.id)

    def perform_destroy(self, instance):
        instance.is_published = False   # 软删除，改为未发布
        instance.save()
        invalidate_article_cache.delay(instance.id)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        点赞/取消点赞接口
        """
        article = self.get_object()
        user = request.user

        # 不能给自己点赞
        if user == article.author:
            return Response({'error': '不能给自己的文章点赞'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'article_like_{article.id}_user_{user.id}'
        liked = cache.get(cache_key)
        if liked is None:
            liked = ArticleLike.objects.filter(user=user, article=article).exists()
            cache.set(cache_key, liked, 3600)

        if liked:
            # 取消点赞
            ArticleLike.objects.filter(user=user, article=article).delete()
            article.likes = max(0, article.likes - 1)
            cache.set(cache_key, False, 3600)
            # 注意：取消点赞不扣回积分，避免刷分（积分仅首次点赞发放）
            article.save(update_fields=['likes'])
            invalidate_article_cache.delay(article.id)
            return Response({'liked': False, 'likes_count': article.likes})
        else:
            ArticleLike.objects.create(user=user, article=article)
            article.likes += 1
            cache.set(cache_key, True, 3600)
            article.save(update_fields=['likes'])
            point_given_key = f'article_like_point_given_{article.id}_user_{user.id}'
            if not cache.get(point_given_key):
                # 未给过积分，增加
                update_points(article.author, 2, 'receive_like', related_id=str(article.id),
                              description=f'文章《{article.title}》收到点赞')
                cache.set(point_given_key, True, 86400 * 365)  # 永久有效
            invalidate_article_cache.delay(article.id)
            return Response({'liked': True, 'likes_count': article.likes})
        