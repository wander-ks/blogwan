from rest_framework import serializers
from users.models import User
from rest_framework.parsers import JSONParser, MultiPartParser
class UserRegisterSerializer(serializers.ModelSerializer):
    """
       用户注册序列化器
       - 自动校验用户名、邮箱唯一性
       - 密码加密存储
   """
    password = serializers.CharField(write_only=True, min_length=6,help_text="密码，至少6位")
    password2 = serializers.CharField(write_only=True, min_length=6,label='确认密码',help_text="确认密码，需与密码一致")

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'bio', 'avatar']
        extra_kwargs = {
            'bio': {'help_text': '个人简介，最多500字'},
            'avatar': {'help_text': '头像图片，支持jpg/png，最大2MB'},
        }

    def validate_username(self, value):
        """校验用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_email(self, value):
        """校验邮箱唯一性"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已被注册")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        return attrs

    def create(self, validated_data):
        # 移除 password2，避免存入数据库
        validated_data.pop('password2')
        user =User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
        用户个人资料序列化器（只读字段自动显示）
    """
    parser_classes = [JSONParser, MultiPartParser]
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'date_joined']
        extra_kwargs = {
            'bio': {'help_text': '个人简介'},
            'avatar': {'help_text': '头像URL'},
        }