from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'author', 'parent', 'content_preview', 'created_at')
    list_filter = ('article', 'author', 'created_at')
    search_fields = ('content', 'author__username', 'article__title')
    raw_id_fields = ('article', 'author', 'parent')
    # date_hierarchy = 'created_at'

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '评论内容'