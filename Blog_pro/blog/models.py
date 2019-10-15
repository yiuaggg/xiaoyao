from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    博客的类别模型
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = {
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    }
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否设为导航')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_created=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    """
    博客的标签模型
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = {
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    }
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM, verbose_name='状态')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_created=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Article(models.Model):
    """
    博客的文章模型
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DARFT = 2
    STATUS_ITEM = {
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DELETE, '草稿'),
    }
    title = models.CharField(max_length=128, verbose_name='标题')
    desc = models.CharField(max_length=1204, verbose_name='摘要')
    content = models.TextField(verbose_name='正文')
    tag = models.ForeignKey(Tag, verbose_name='标签', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM, verbose_name='状态')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_created=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']