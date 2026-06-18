"""
Django Admin — для ER-диаграммы и проверки БД (критерий Д2Д1, Ж2Д1).
На экзамене основная панель — portal/admin/dashboard.html.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Application, Review, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "full_name", "email", "phone", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("full_name", "phone")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("full_name", "phone", "email")}),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course_name", "start_date", "payment_method", "status")
    list_filter = ("status", "payment_method")
    search_fields = ("course_name", "user__username")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("application", "rating", "created_at")
