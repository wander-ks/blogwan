from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()

class Comment(models.Model):
    """
    评论模型，支持嵌套回复（通过 parent 外键自关联）
    """
    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='所属文章'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='评论作者'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='父评论'
    )
    content = models.TextField('评论内容', max_length=500)
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'comments_comment'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['article', 'created_at']),
            models.Index(fields=['author']),
        ]
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'{self.author.username} 评论了 {self.article.title}'