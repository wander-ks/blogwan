from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from interactions.models import ArticleLike
from interactions.serializers import ArticleLikeSerializer
from articles.models import Article
from django.core.cache import cache

class UserLikedArticlesView(generics.ListAPIView):
    """
    获取当前用户点赞过的文章列表
    """
    serializer_class = ArticleLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ArticleLike.objects.filter(user=self.request.user).select_related('article')


class ArticleLikeStatusView(APIView):
    """
    检查当前用户是否点赞了某篇文章
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, article_id):
        # 优先使用 Redis 缓存
        cache_key = f'article_like_{article_id}_user_{request.user.id}'
        liked = cache.get(cache_key)
        if liked is None:
            liked = ArticleLike.objects.filter(user=request.user, article_id=article_id).exists()
            cache.set(cache_key, liked, 3600)
        return Response({'liked': liked})