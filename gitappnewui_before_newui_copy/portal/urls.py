from django.urls import path

from . import views

app_name = "portal"

urlpatterns = [
    path("", views.home, name="home"),
    # Авторизация и регистрация
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Заявки пользователя
    path("applications/", views.application_list_view, name="application_list"),
    path("applications/new/", views.application_create_view, name="application_create"),
    # Панель администратора (отдельный модуль — другой дизайн)
    path("admin-panel/login/", views.admin_login_view, name="admin_login"),
    path("admin-panel/logout/", views.admin_logout_view, name="admin_logout"),
    path("admin-panel/", views.admin_dashboard_view, name="admin_dashboard"),
]
