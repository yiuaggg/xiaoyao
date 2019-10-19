from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    针对queryset过滤当前用户
    因为很多地方用到所以把它写到这里
    """
    exclude = ('author',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)