from django.contrib import admin

# Register your models here.

from articles.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'views', 'likes', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('views', 'likes', 'created_at', 'updated_at')
    # date_hierarchy = 'created_at'