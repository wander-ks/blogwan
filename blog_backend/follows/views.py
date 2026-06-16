from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from follows.models import Follow
from follows.serializers import FollowSerializer
from follows.redis_utils import add_follow, remove_follow, is_following

User = get_user_model()

class FollowViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    @action(detail=False, methods=['post'], url_path='follow/(?P<user_id>[^/.]+)')
    def follow_user(self, request, user_id):
        if request.user.id == int(user_id):
            return Response({'error': '不能关注自己'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            followed_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        if is_following(request.user.id, user_id):
            return Response({'error': '已经关注过了'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Follow.objects.create(user=request.user, followed_user=followed_user)
            add_follow(request.user.id, int(user_id))
            return Response({'status': '关注成功', 'is_following': True}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': '关注关系已存在'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='unfollow/(?P<user_id>[^/.]+)')
    def unfollow_user(self, request, user_id):
        try:
            follow = Follow.objects.get(user=request.user, followed_user_id=user_id)
            follow.delete()
            remove_follow(request.user.id, int(user_id))
            return Response({'status': '取消关注成功', 'is_following': False})
        except Follow.DoesNotExist:
            return Response({'error': '尚未关注'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def following_list(self, request):
        queryset = Follow.objects.filter(user=request.user).select_related('followed_user')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def follower_list(self, request):
        follows = Follow.objects.filter(followed_user=request.user).select_related('user')
        serializer = self.get_serializer(follows, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='status/(?P<user_id>[^/.]+)')
    def follow_status(self, request, user_id):
        following = is_following(request.user.id, int(user_id))
        return Response({'is_following': following})