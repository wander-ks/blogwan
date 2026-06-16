from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class UserPoints(models.Model):
    """用户积分"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='points')
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
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sign_records')
    sign_date = models.DateField('签到日期', default=timezone.now)
    month = models.CharField('年月', max_length=7, help_text='格式 YYYY-MM')
    points_gained = models.IntegerField('获得积分', default=1)

    class Meta:
        db_table = 'points_sign_in_record'
        unique_together = ('user', 'sign_date')
        indexes = [
            models.Index(fields=['user', 'month']),
        ]
        verbose_name = '签到记录'
        verbose_name_plural = '签到记录'

class Festival(models.Model):
    """节日配置"""
    name = models.CharField('节日名称', max_length=50)
    month = models.IntegerField('月份')
    day = models.IntegerField('日期')
    bonus_points = models.IntegerField('赠送积分', default=10)

    class Meta:
        db_table = 'points_festival'
        verbose_name = '节日配置'
        verbose_name_plural = '节日配置'

class UserFestivalReceiveLog(models.Model):
    """
    用户节日积分领取记录，防止重复发放
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    festival = models.ForeignKey("Festival", on_delete=models.CASCADE)
    receive_date = models.DateField('领取时间',auto_now_add=True)

    class Meta:
        db_table = 'User_festival_receiveLog'
        unique_together = ("user", "festival", "receive_date")
        verbose_name = "节日积分领取记录"



