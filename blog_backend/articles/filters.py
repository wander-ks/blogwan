from django_filters import rest_framework as filters
from articles.models import Article

class ArticleFilter(filters.FilterSet):
    """
    文章过滤器：按作者用户名、发布时间范围、标题关键词等
    """
    author__username = filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    title_contains = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['author__username', 'is_published']