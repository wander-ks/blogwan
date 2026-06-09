from celery import shared_task
from django.core.cache import cache
from django.db.models import F
from articles.models import Article
from django.contrib.auth import get_user_model
from notifications.models import Message
from follows.redis_utils import get_following_ids   # 粉丝列表
@shared_task
def increase_views_async(article_id, ip_address):
    cache_key = f'article_view_{article_id}_{ip_address}'
    if cache.get(cache_key):
        return
    cache.set(cache_key, 1, 300)
    Article.objects.filter(id=article_id).update(views=F('views') + 1)

@shared_task
def invalidate_article_cache(article_id):
    cache.delete_pattern(f'article_detail_{article_id}_*')

@shared_task
def rebuild_article_list_cache():
    pass



def get_follower_ids(user_id):
    """获取用户的粉丝 ID 列表（从 Redis 或数据库）"""
    # 简单实现：从数据库获取，也可以缓存 Redis Set 存储粉丝
    from follows.models import Follow
    return list(Follow.objects.filter(followed_user_id=user_id).values_list('user_id', flat=True))

@shared_task
def send_new_article_notification(article_id, author_id, article_title):
    """文章发布后给所有粉丝发送站内信"""
    from articles.models import Article
    try:
        article = Article.objects.get(id=article_id)
        author = get_user_model().objects.get(id=author_id)
        # 获取粉丝 ID 列表
        follower_ids = get_follower_ids(author_id)
        if not follower_ids:
            return f'No followers for user {author_id}'
        # 批量创建站内信
        messages = []
        for follower_id in follower_ids:
            messages.append(Message(
                recipient_id=follower_id,
                sender=author,
                message_type='system',
                title=f'{author.username} 发布了新文章',
                content=article_title,
                link=f'/articles/{article_id}'
            ))
        Message.objects.bulk_create(messages)
        return f'Notified {len(messages)} followers'
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Failed to send article notifications: {e}')
        return str(e)