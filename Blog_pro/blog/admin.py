from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Category, Tag, Article
from .adminforms import ArticleAdminForm

from utils.custom_site import custom_site
from utils.base_admin import BaseOwnerAdmin


class ArticleInline(admin.StackedInline):
    """
    展示样式
    """
    fields = ('title', 'desc')
    extra = 1
    model = Article


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    """
    分类后台
    """
    inlines = [ArticleInline]
    list_display = ('name', 'status', 'is_nav', 'create_time', 'author')
    fields = ('name', 'status', 'is_nav')

    def article_count(self, obj):
        return obj.post_set.count()

    article_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    """
    标签后台
    """
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器过滤除了自己的用户分类
    为了让每个用户只看到自己的文章信息
    """
    title = '分类'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(author=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Article, site=custom_site)
class ArticleAdmin(BaseOwnerAdmin):
    """
    文章后台
    """
    list_display = [
        'title', 'category', 'status', 'create_time', 'author', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    # 编辑页面
    exclude = ['author']
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('tag',),
        })
    )
    filter_vertical = ('tag',)

    # 同页面编辑需求实现
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_article_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    class Media:
        """
        引用bootstrap样式
        """
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta/css/bootstrap.min.css",),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'object_repr', 'object_id', 'action_flag', 'user', 'change_message'
    ]
