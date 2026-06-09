from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from comments.models import Comment
from comments.serializers import CommentSerializer, CommentWriteSerializer
from comments.permissions import IsAuthorOrAdminOrArticleAuthor
from comments.tasks import send_comment_notification
from comments.filters import CommentFilter
class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集：
    - list: 按文章ID获取顶级评论（parent=None）
    - create: 发表评论（需登录）
    - update/destroy: 权限控制
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrArticleAuthor]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CommentFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # 返回所有评论，让过滤器决定
        return Comment.objects.all().select_related('author', 'article')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentWriteSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # 发送通知（站内信）
        parent = comment.parent
        if parent:
            send_comment_notification.delay(
                article_id=comment.article.id,
                comment_id=comment.id,
                parent_author_id=parent.author.id
            )
        else:
            send_comment_notification.delay(
                article_id=comment.article.id,
                comment_id=comment.id,
                parent_author_id=None
            )