import django_filters
from comments.models import Comment

class CommentFilter(django_filters.FilterSet):
    # 支持 ?parent=null 获取顶级评论
    parent = django_filters.CharFilter(method='filter_parent')

    def filter_parent(self, queryset, name, value):
        if value == 'null':
            return queryset.filter(parent__isnull=True)
        return queryset.filter(parent_id=value)

    class Meta:
        model = Comment
        fields = ['article']