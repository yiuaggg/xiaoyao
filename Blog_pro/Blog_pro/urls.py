"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from utils.custom_site import custom_site
from blog.views import article_list, article_detail
from config.views import links

urlpatterns = [
    path('', article_list),
    path('category/<int:category_id>', article_list),
    path('tag/<int:tag_id>', article_list),
    path('article/<int:article_id>', article_detail),
    path('links/', links),
    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
]
