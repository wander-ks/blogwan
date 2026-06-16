from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    自定义用户模型，扩展 Django 默认的 auth_user 表
    """
    bio = models.TextField('个人简介', max_length=500, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)

    class Meta:
        db_table = 'users_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username