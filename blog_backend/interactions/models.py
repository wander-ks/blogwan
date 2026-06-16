from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
class ArticleLike(models.Model):
    """
    记录用户对文章的点赞关系，防止重复点赞
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liked_articles',
        verbose_name='用户'
    )
    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
        related_name='liked_users',
        verbose_name='文章'
    )
    created_at = models.DateTimeField('点赞时间', auto_now_add=True)

    class Meta:
        db_table = 'interactions_articlelike'
        unique_together = ('user', 'article')
        verbose_name = '文章点赞'
        verbose_name_plural = '文章点赞'

    def __str__(self):
        return f'{self.user.username} 点赞了 {self.article.title}'