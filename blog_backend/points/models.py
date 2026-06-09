from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone

class UserPoints(models.Model):
    """用户积分总览（冗余，便于快速查询）"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='points')
    balance = models.IntegerField('积分余额', default=0)
    total_earned = models.IntegerField('累计获得积分', default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'points_user_points'
        verbose_name = '用户积分'
        verbose_name_plural = '用户积分'

class PointsTransaction(models.Model):
    """积分流水记录"""
    TRANSACTION_TYPES = (
        ('sign_in', '每日签到'),
        ('sign_bonus', '满月奖励'),
        ('festival', '节日福利'),
        ('publish_article', '发布文章'),
        ('receive_like', '收到点赞'),
        ('download_pay', '下载支付'),
        ('download_income', '下载收入'),
        ('admin_adjust', '管理员调整'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField('变动数量（正为获得，负为消耗）')
    transaction_type = models.CharField('类型', max_length=30, choices=TRANSACTION_TYPES)
    related_object_id = models.CharField('关联对象ID', max_length=50, blank=True, help_text='如文章ID、签到记录ID')
    description = models.CharField('描述', max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'points_points_transaction'
        ordering = ['-created_at']
        verbose_name = '积分流水'
        verbose_name_plural = '积分流水'

class SignInRecord(models.Model):
    """签到记录"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sign_records')
    sign_date = models.DateField('签到日期', default=timezone.now)
    month = models.CharField('年月', max_length=7, help_text='格式 YYYY-MM')
    points_gained = models.IntegerField('获得积分', default=1)

    class Meta:
        db_table = 'points_sign_in_record'
        unique_together = ('user', 'sign_date')
        indexes = [
            models.Index(fields=['user', 'month']),
        ]

class Festival(models.Model):
    """节日配置（可选，用于定时发放福利）"""
    name = models.CharField('节日名称', max_length=50)
    month = models.IntegerField('月份')
    day = models.IntegerField('日期')
    bonus_points = models.IntegerField('赠送积分', default=10)

    class Meta:
        db_table = 'points_festival'