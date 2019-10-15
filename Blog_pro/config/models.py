from django.contrib.auth.models import User
from django.db import models


class Link(models.Model):
    """
    博客的分享链接模型
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = {
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    }
    title = models.CharField(max_length=50, verbose_name='标题')
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM, verbose_name='状态')
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)), verbose_name='权重')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分享链接'


class SideBar(models.Model):
    """
    博客的侧边栏模型
    """
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEM = {
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    }
    SIDE_TYPE = (
        (1, 'HTML'),
        (2, '最新'),
        (3, '最热'),
        (4, '最近评论')
    )
    title = models.CharField(max_length=50, verbose_name='标题')
    display_type = models.PositiveIntegerField(default=1, choices=STATUS_ITEM, verbose_name='展示类型')
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEM, verbose_name='状态')
    content = models.CharField(max_length=500, blank=True, verbose_name='内容')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'

