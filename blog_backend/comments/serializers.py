from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    评论序列化器：用于 GET 请求（列表、详情），支持递归展示子评论（replies）
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)
    reply_count = serializers.IntegerField(source='replies.count', read_only=True)
    replies = serializers.SerializerMethodField()
    def __init__(self, *args, depth=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth = depth


    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'article_title', 'author', 'author_name',
            'parent', 'content', 'created_at', 'updated_at', 'reply_count','replies'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if self.depth >= 3:
            return []
        queryset = obj.replies.all().select_related("author")
        if not queryset.exists():
            return []
        ser = CommentSerializer(queryset, many=True,depth=self.depth + 1)
        return ser.data


class CommentWriteSerializer(serializers.ModelSerializer):
    """
    评论写序列化器（用于创建，不展示嵌套回复）
    """
    class Meta:
        model = Comment
        fields = ['article', 'parent', 'content']