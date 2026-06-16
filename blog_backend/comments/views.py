from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from comments.models import Comment
from comments.serializers import CommentSerializer, CommentWriteSerializer
from comments.tasks import send_comment_notification
from comments.filters import CommentFilter
from users.permissions import IsOwnerOrReadOnly
class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集，提供：
    - list   : GET /comments/          可过滤 ?article=1 获取顶级评论，或 ?parent=5 获取子评论
    - create : POST /comments/         发表评论（需认证）
    - retrieve: GET /comments/{id}/    获取单条评论详情
    - update : PUT /comments/{id}/     更新评论（仅作者）
    - destroy: DELETE /comments/{id}/  删除评论（作者/管理员/文章作者）
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CommentFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
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