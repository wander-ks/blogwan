from celery import shared_task
from django.contrib.auth import get_user_model
from notifications.models import Message

User = get_user_model()

@shared_task
def send_new_article_notification(article_id, author_id, article_title):
    """文章发布后给所有粉丝发送站内信"""
    from articles.models import Article
    try:
        article = Article.objects.get(id=article_id)
        author = User.objects.get(id=author_id)

        from follows.models import Follow
        follower_ids = list(Follow.objects.filter(followed_user_id=author_id).values_list('user_id', flat=True))
        if not follower_ids:
            return f'No followers for user {author_id}'
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