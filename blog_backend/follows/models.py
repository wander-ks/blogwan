from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Follow(models.Model):
    """关注关系表"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='用户'
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='被关注用户'
    )
    created_at = models.DateTimeField('关注时间', auto_now_add=True)

    class Meta:
        db_table = 'follows_follow'
        unique_together = ('user', 'followed_user')
        verbose_name = '关注关系'
        verbose_name_plural = '关注关系'

    def __str__(self):
        return f'{self.user.username} 关注了 {self.followed_user.username}'