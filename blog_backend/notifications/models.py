from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Message(models.Model):
    """
    站内信消息模型
    类型：欢迎消息、评论通知、点赞通知等
    """
    MESSAGE_TYPES = (
        ('welcome', '欢迎消息'),
        ('comment', '评论通知'),
        ('reply', '回复通知'),
        ('like', '点赞通知'),
        ('system', '系统消息'),
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='收件人'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_messages',
        verbose_name='发件人'
    )
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='system')
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    link = models.CharField(max_length=200, blank=True, help_text='关联链接（如文章详情页）')

    class Meta:
        db_table = 'notifications_message'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
        verbose_name = '站内信'
        verbose_name_plural = '站内信'

    def __str__(self):
        return f'{self.title} to {self.recipient.username}'