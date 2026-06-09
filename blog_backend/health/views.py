from django.shortcuts import render

# Create your views here.
# apps/health/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connections
from django.core.cache import cache
from celery import current_app

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    status = {
        'status': 'ok',
        'db': 'ok',
        'cache': 'ok',
        'celery': 'ok'
    }
    # 检查数据库
    try:
        connections['default'].cursor()
    except Exception:
        status['db'] = 'error'
        status['status'] = 'degraded'
    # 检查 Redis
    try:
        cache.get('health_test')
    except Exception:
        status['cache'] = 'error'
        status['status'] = 'degraded'
    # 检查 Celery
    try:
        current_app.broker_connection().ensure_connection(max_retries=1)
    except Exception:
        status['celery'] = 'error'
        status['status'] = 'degraded'
    return Response(status, status=200 if status['status'] == 'ok' else 500)