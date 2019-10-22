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
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories
        }


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
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


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
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM, verbose_name='状态')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            article_list = None
        else:
            article_list = tag.article_set.filter(status=Article.STATUS_NORMAL)\
                .select_related('author', 'category')

        return article_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            article_list = []
        else:
            article_list = category.article_set.filter(status=Article.STATUS_NORMAL)\
                .select_related('author', 'category')

        return article_list, category

    @classmethod
    def latest_article(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_articles(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('pv')
