from rest_framework import serializers
from notifications.models import Message

class MessageSerializer(serializers.ModelSerializer):
    """
    站内信序列化器，用于列表和详情展示
    """
    sender_name = serializers.CharField(source='sender.username', read_only=True, default='系统')

    class Meta:
        model = Message
        fields = ['id', 'title', 'content', 'message_type', 'is_read', 'created_at', 'link', 'sender_name']
        read_only_fields = ['id', 'created_at']