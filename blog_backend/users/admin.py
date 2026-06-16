from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


admin.site.site_header = '博客后台管理系统'
admin.site.site_title = '博客管理'
admin.site.index_title = '欢迎使用博客管理后台'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'bio', 'avatar', 'date_joined')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('bio', 'avatar',)}),
    )


