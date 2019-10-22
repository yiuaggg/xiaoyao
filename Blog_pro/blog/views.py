from django.shortcuts import render
from .models import Article, Tag, Category
from config.models import SideBar


def article_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        article_list, tag = Article.get_by_tag(tag_id)
    elif category_id:
        article_list, category = Article.get_by_category(category_id)
    else:
        article_list = Article.latest_article()

    context = {
        'category': category,
        'tag': tag,
        'article_list': article_list,
        'sidebars': SideBar.get_all(),
    }

    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def article_detail(request, article_id=None):
    try:
        article = Article.objects.get(id=article_id)
    except article.DoesNotExist:
        article = None

    context = {
        'article': article,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
