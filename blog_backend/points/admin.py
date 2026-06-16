from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserPoints, PointsTransaction, SignInRecord, Festival

@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_earned', 'updated_at')
    search_fields = ('user__username',)
    # date_hierarchy = 'updated_at'
    list_per_page = 9

@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username',)
    # date_hierarchy = 'created_at'
    list_per_page = 9

@admin.register(SignInRecord)
class SignInRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'sign_date', 'month', 'points_gained')
    list_filter = ('month',)
    date_hierarchy = 'sign_date'
    list_per_page = 9

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'month', 'day', 'bonus_points')
    list_per_page = 9