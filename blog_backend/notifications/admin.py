from django.contrib import admin

# Register your models here.
from django.contrib import admin
from notifications.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'recipient', 'sender', 'message_type', 'is_read', 'created_at')
    list_filter = ('message_type', 'is_read', 'created_at')
    search_fields = ('title', 'content', 'recipient__username', 'sender__username')
    raw_id_fields = ('recipient', 'sender')
    readonly_fields = ('created_at',)
    # date_hierarchy = 'created_at'