from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.models import Message
from notifications.serializers import MessageSerializer

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
        站内信视图集，提供只读操作 + 标记已读/删除。
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('is_read', '-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        message = self.get_object()
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        """标记当前用户所有未读消息为已读"""
        count = Message.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'marked_count': count})