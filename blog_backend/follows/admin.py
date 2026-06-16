from django.contrib import admin

from django.contrib import admin
from .models import Follow

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'followed_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'followed_user__username')
    raw_id_fields = ('user', 'followed_user')
    # date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def user_info(self, obj):
        return obj.user.username
    user_info.short_description = '关注者'

    def followed_info(self, obj):
        return obj.followed_user.username
    followed_info.short_description = '被关注者'