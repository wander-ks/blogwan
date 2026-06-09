from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from notifications.models import Message
from points.models import SignInRecord, Festival, UserPoints
from points.services import update_points

User = get_user_model()

@shared_task
def send_daily_sign_reminder():
    """每天8点向所有用户发送签到提醒站内信"""
    users = User.objects.all()
    for user in users:
        # 检查今天是否已经签到
        today = timezone.now().date()
        if not SignInRecord.objects.filter(user=user, sign_date=today).exists():
            Message.objects.create(
                recipient=user,
                message_type='system',
                title='每日签到提醒',
                content='今日尚未签到，快点击导航栏“签到”按钮领取积分吧！',
                link='/'
            )
    return f'Reminder sent to {users.count()} users'

@shared_task
def check_festival_bonus():
    """检查当天是否有节日，若有则给所有用户发放积分"""
    today = timezone.now()
    month, day = today.month, today.day
    festivals = Festival.objects.filter(month=month, day=day)
    if not festivals:
        return 'No festival today'
    for festival in festivals:
        users = User.objects.all()
        for user in users:
            update_points(user, festival.bonus_points, 'festival', description=f'{festival.name}福利')
        return f'Festival bonus {festival.bonus_points} points sent to {users.count()} users'