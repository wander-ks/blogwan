# points/utils.py
import uuid
from django.core.cache import cache

def generate_download_token(article_id, user_id):
    """生成一次性下载 token，有效期 1 小时"""
    token = str(uuid.uuid4())
    cache_key = f'download_token:{token}'
    cache.set(cache_key, {'article_id': article_id, 'user_id': user_id}, timeout=3600)
    return token

def consume_download_token(token):
    """验证并消费 token，返回文章 ID 和用户 ID，若无效返回 None"""
    cache_key = f'download_token:{token}'
    data = cache.get(cache_key)
    if data:
        cache.delete(cache_key)
        return data['article_id'], data['user_id']
    return None, None