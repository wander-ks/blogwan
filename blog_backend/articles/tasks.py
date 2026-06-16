from celery import shared_task
from django.core.cache import cache
from django.db.models import F
from articles.models import Article
from django.contrib.auth import get_user_model
User = get_user_model()

@shared_task
def increase_views_async(article_id, ip_address):
    """
    异步增加文章阅读量，基于 IP 防刷（5分钟内同一 IP 只计数一次）
    """
    cache_key = f'article_view_{article_id}_{ip_address}'
    if cache.get(cache_key):
        return
    cache.set(cache_key, 1, 300)
    Article.objects.filter(id=article_id).update(views=F('views') + 1)

@shared_task
def invalidate_article_cache(article_id):
    """
    当文章被更新或删除时，清除该文章的详情缓存
    """
    cache.delete_pattern(f'article_detail_{article_id}_*')