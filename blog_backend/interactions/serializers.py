from rest_framework import serializers
from interactions.models import ArticleLike

class ArticleLikeSerializer(serializers.ModelSerializer):
    """
    点赞关系序列化器（用于展示用户点赞历史）
    """
    username = serializers.CharField(source='user.username', read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)
    article_id = serializers.IntegerField(source='article.id', read_only=True)
    class Meta:
        model = ArticleLike
        fields = ['id', 'username', 'article_id', 'article_title', 'created_at']
        read_only_fields = ['id', 'created_at']