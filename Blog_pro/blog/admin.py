from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Category, Tag, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'create_time', 'author')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'create_time', 'operator'
    ]
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag'
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_article_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(ArticleAdmin, self).save_model(request, obj, form, change)