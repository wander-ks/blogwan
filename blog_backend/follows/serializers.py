from rest_framework import serializers
from follows.models import Follow
from users.serializers import UserProfileSerializer

class FollowSerializer(serializers.ModelSerializer):
    user_info = UserProfileSerializer(source='user', read_only=True)
    followed_user_info = UserProfileSerializer(source='followed_user', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'user', 'user_info', 'followed_user', 'followed_user_info', 'created_at']
        read_only_fields = ['id', 'created_at','user']