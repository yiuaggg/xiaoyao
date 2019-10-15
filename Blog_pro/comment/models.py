from django.db import models
from blog.models import Article
from django.contrib.auth.models import User


class Comment(models.Model):
    """
    博客的评论模型
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = {
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    }
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    target = models.ForeignKey(Article, verbose_name='评论目标', on_delete=models.CASCADE)
    content = models.CharField(max_length=1024, verbose_name='评论内容')
    commenter = models.ForeignKey(User, verbose_name='评论者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '评论'
