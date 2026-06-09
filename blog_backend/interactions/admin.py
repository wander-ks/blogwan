from django.contrib import admin

# Register your models here.
from interactions.models import ArticleLike

@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'article', 'created_at')
    list_filter = ('user', 'article')
    search_fields = ('user__username', 'article__title')