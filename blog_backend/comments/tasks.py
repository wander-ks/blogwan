from celery import shared_task
from notifications.models import Message

@shared_task
def send_comment_notification(article_id, comment_id, parent_author_id=None):
    """
    发送评论通知站内信
    """
    from django.contrib.auth import get_user_model
    from articles.models import Article
    from comments.models import Comment

    User = get_user_model()
    try:
        comment = Comment.objects.select_related('author', 'article').get(id=comment_id)
        article = comment.article
        if parent_author_id:
            target_user = User.objects.get(id=parent_author_id)
            is_reply = True
        else:
            target_user = article.author
            is_reply = False

        if target_user == comment.author:
            return

        if is_reply:
            title = f'{comment.author.username} 回复了您的评论'
            content = f'在文章《{article.title}》中：\n"{comment.parent.content[:100]}..."\n回复内容：{comment.content[:200]}'
            link = f'/articles/{article.id}#comment-{comment.id}'
        else:
            title = f'{comment.author.username} 评论了您的文章《{article.title}》'
            content = f'评论内容：{comment.content[:200]}'
            link = f'/articles/{article.id}#comment-{comment.id}'

        Message.objects.create(
            recipient=target_user,
            sender=comment.author,
            message_type='comment' if not is_reply else 'reply',
            title=title,
            content=content,
            link=link
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Failed to send comment notification: {e}')