from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from users.serializers import UserRegisterSerializer, UserProfileSerializer
from users.models import User
from users.tasks import send_welcome_message
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


class RegisterView(generics.CreateAPIView):
    """
    用户注册端点
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        tags=['用户认证'],
        summary='用户注册',
        description='创建新账号，用户名和邮箱必须唯一，密码至少6位。注册成功后异步发送欢迎站内信。',
        request=UserRegisterSerializer,
        responses={
            201: OpenApiResponse(description='注册成功', response=UserRegisterSerializer),
            400: OpenApiResponse(description='请求参数错误（用户名/邮箱重复、密码不一致等）'),
        },
        examples=[
            OpenApiExample(
                '注册请求示例',
                value={
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'password': 'secure123',
                    'password2': 'secure123',
                    'bio': '技术爱好者',
                },
                request_only=True,
            ),
            OpenApiExample(
                '注册成功响应示例',
                value={
                    'id': 5,
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'bio': '技术爱好者',
                    'avatar': None,
                },
                response_only=True,
            ),
        ]
    )
    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_message.delay(user.id, user.username)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    用户个人资料获取与更新
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser,MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user