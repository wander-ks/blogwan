from rest_framework import serializers
from articles.models import Article
from users.serializers import UserProfileSerializer

class ArticleListSerializer(serializers.ModelSerializer):
    """
    文章列表序列化器（用于分页列表展示）
    """
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'cover_image', 'author_name', 'created_at', 'views', 'likes']


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    文章详情序列化器（包含作者详细信息）
    """
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'views', 'likes']


class ArticleWriteSerializer(serializers.ModelSerializer):
    """
    文章写序列化器（用于创建/更新，不展示只读字段）
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'cover_image', 'is_published']