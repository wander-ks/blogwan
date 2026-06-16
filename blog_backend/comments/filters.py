import django_filters
from comments.models import Comment

class CommentFilter(django_filters.FilterSet):
    parent = django_filters.CharFilter(method='filter_parent')
    article = django_filters.NumberFilter(field_name="article_id")

    def filter_parent(self, queryset, name, value):
        if value.strip().lower() in ('null', 'None', ''):
            return queryset.filter(parent__isnull=True)
        if value.isdigit():
            return queryset.filter(parent_id=int(value))
        return queryset.none()
    class Meta:
        model = Comment
        fields = ['article', 'parent']