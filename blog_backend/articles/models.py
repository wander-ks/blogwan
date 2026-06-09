from django.db import models

# Create your models here.
from django.conf import settings

class Article(models.Model):
    """
    文章模型
    """
    title = models.CharField('标题', max_length=200, db_index=True)
    content = models.TextField('正文')
    cover_image = models.ImageField('封面图', upload_to='covers/', blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='作者'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    views = models.PositiveIntegerField('阅读量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    is_published = models.BooleanField('是否发布', default=True)

    class Meta:
        db_table = 'articles_article'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title