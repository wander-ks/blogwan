
from functools import wraps
from django.core.cache import cache

def cached(ttl=300, key_prefix=''):
    """
    缓存函数返回值的装饰器
    用法: @cached(ttl=60, key_prefix='my_key')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 根据函数名和参数生成唯一 key
            key = f'{key_prefix}_{func.__name__}_{str(args)}_{str(kwargs)}'
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator