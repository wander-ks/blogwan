"""blog_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from articles.views import download_file
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # OpenAPI schema 文件（JSON/YAML）
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI 交互文档
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc 文档
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/v1/articles/download-file/', download_file, name='download_file'),
    path('admin/', admin.site.urls),
    re_path(r'^api/v1/auth/',include('users.urls')),
    re_path(r'^api/v1/',include('articles.urls')),
    re_path(r'^api/v1/',include('comments.urls')),
    re_path(r'^api/v1/',include('follows.urls')),
    re_path(r'^api/v1/notifications/', include('notifications.urls')),
    re_path(r'^api/v1/points/', include('points.urls')),

]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)