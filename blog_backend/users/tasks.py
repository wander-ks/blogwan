from celery import shared_task
from notifications.models import Message

@shared_task
def send_welcome_message(user_id, username):
    """
    异步发送欢迎站内信
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        Message.objects.create(
            recipient=user,
            message_type='welcome',
            title=f'欢迎加入 BlogWan，{username}！',
            content='感谢您注册博客平台。在这里您可以发布技术文章、参与讨论。祝您使用愉快！',
            link='/'
        )
    except User.DoesNotExist:
        pass