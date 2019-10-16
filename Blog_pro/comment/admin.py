from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    评论后台
    """
    list_display = (
        'target', 'commenter', 'status', 'content', 'create_time'
    )
