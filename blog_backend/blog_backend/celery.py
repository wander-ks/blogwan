import os
from celery import Celery

# 设置 Django 配置模块（根据环境调整）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')

app = Celery('blog_backend')

# 从 Django 设置中加载 Celery 配置（命名空间以 CELERY 开头）
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有已注册 Django app 中的 tasks.py
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

from celery.schedules import crontab

# 定时任务调度（Celery Beat）
CELERY_BEAT_SCHEDULE = {
    # 每5分钟同步点赞计数
    'sync-likes-every-5-minutes': {
        'task': 'interactions.tasks.sync_likes_from_redis',
        'schedule': 300,   # 秒，也可以用 crontab
    },

    # 每5分钟批量保存点赞关系明细
    # 'sync-save-every-5-minutes': {
    #     'task': 'interactions.tasks.batch_save_like_relations',
    #     'schedule': 300,
    # },

    # 每天8点向所有用户发送签到提醒站内信
    'send-daily-sign-reminder': {
        'task': 'points.tasks.send_daily_sign_reminder',
        'schedule': crontab(hour=8, minute=0),
    },

    # 检查当天是否有节日，若有则给所有用户发放积分
    'check-festival-bonus': {
        'task': 'points.tasks.check_festival_bonus',
        'schedule': crontab(hour=8, minute=0),
    },
}