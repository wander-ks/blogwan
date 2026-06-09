from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    评论序列化器：支持嵌套回复（递归展示 replies）
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)
    reply_count = serializers.IntegerField(source='replies.count', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'article_title', 'author', 'author_name',
            'parent', 'content', 'created_at', 'updated_at', 'reply_count'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_replies(self, obj):
        # 递归序列化子评论
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    def create(self, validated_data):
        # 自动设置 author 为当前请求用户（在视图中处理）
        return super().create(validated_data)


class CommentWriteSerializer(serializers.ModelSerializer):
    """
    评论写序列化器（用于创建，不展示嵌套回复）
    """
    class Meta:
        model = Comment
        fields = ['article', 'parent', 'content']