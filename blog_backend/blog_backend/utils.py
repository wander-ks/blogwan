
from rest_framework.response import Response

class APIResponse(Response):
    """
    统一 API 响应格式：
    {
        "code": 200,
        "message": "success",
        "data": {...}
    }
    """
    def __init__(self, data=None, code=200, message='success', status=None, **kwargs):
        if data is None:
            data = {}
        response_data = {
            'code': code,
            'message': message,
            'data': data
        }
        super().__init__(data=response_data, status=status or code, **kwargs)

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    自定义 DRF 异常处理器，返回统一格式
    """
    response = exception_handler(exc, context)
    if response is not None:
        # 将 DRF 默认的错误结构转换为统一格式
        return Response({
            'code': response.status_code,
            'message': response.data.get('detail') or 'Error',
            'data': response.data
        }, status=response.status_code)
    # 未处理的异常返回 500
    return Response({
        'code': 500,
        'message': 'Internal Server Error',
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 时间工具函数
from datetime import datetime
import pytz

def format_datetime(dt, tz='Asia/Shanghai'):
    """将 datetime 转换为指定时区的字符串"""
    if dt.tzinfo is None:
        dt = pytz.timezone(tz).localize(dt)
    else:
        dt = dt.astimezone(pytz.timezone(tz))
    return dt.strftime('%Y-%m-%d %H:%M:%S')