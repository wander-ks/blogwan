import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django.request')

class RequestLogMiddleware(MiddlewareMixin):
    """
    记录请求日志：方法、路径、状态码、耗时、IP
    """
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            ip = self.get_client_ip(request)
            logger.info(
                f'{request.method} {request.build_absolute_uri()} '
                f'{response.status_code} {duration:.2f}s {ip}'
            )
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip



class PerformanceMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            if duration > 1:  # 超过1秒的请求记录警告
                logger.warning(f'Slow request: {request.path} took {duration:.2f}s')
        return response


from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class ExceptionMiddleware(MiddlewareMixin):
    """
    全局异常捕获，返回统一 JSON 格式
    """
    def process_exception(self, request, exception):
        # 记录错误日志（可结合 logging）
        import traceback
        traceback.print_exc()
        return JsonResponse(
            {'error': str(exception), 'code': 500},
            status=500
        )