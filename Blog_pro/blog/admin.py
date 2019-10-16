from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Category, Tag, Article
from Blog_pro.custom_site import custom_site


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
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'create_time', 'author', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    # actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True

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
            reverse('cus_admin:blog_article_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(ArticleAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        return qs.filter(author=request.user)

    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta/css/bootstrap.min.css",),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)