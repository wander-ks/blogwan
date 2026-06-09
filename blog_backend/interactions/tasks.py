from celery import shared_task
from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from articles.models import Article

@shared_task
def sync_likes_from_redis():
    from django_redis import get_redis_connection
    conn = get_redis_connection('default')
    keys = conn.keys('article_like_count_*')
    updated = 0
    for key in keys:
        article_id = int(key.decode().split('_')[-1])
        count = conn.get(key)
        if count:
            count = int(count)
            Article.objects.filter(id=article_id).update(likes=F('likes') + count)
            conn.delete(key)
            updated += 1
    return f'Synced {updated} articles'