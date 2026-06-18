"""
Представления всех разделов ИС.
Модуль 1: базовый функционал. Модуль 2: валидация на форме, фильтры в админке.
"""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from exam_config import ADMIN_LOGIN, ADMIN_PASSWORD

from .decorators import admin_session_required, login_required_custom
from .forms import (
    AdminLoginForm,
    AdminStatusForm,
    ApplicationForm,
    LoginForm,
    RegistrationForm,
    ReviewForm,
)
from .models import Application, Review


def home(request):
    """Главная — редирект в зависимости от роли."""
    if request.session.get("is_portal_admin"):
        return redirect("portal:admin_dashboard")
    if request.user.is_authenticated:
        return redirect("portal:application_list")
    return redirect("portal:login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("portal:application_list")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация прошла успешно. Добро пожаловать!")
        return redirect("portal:application_list")

    return render(request, "portal/auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("portal:application_list")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Вы успешно вошли в систему.")
            return redirect("portal:application_list")
        messages.error(request, "Неверный логин или пароль.")

    return render(request, "portal/auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("portal:login")


@login_required_custom
def application_list_view(request):
    """Просмотр заявок пользователя + отзывы."""
    applications = Application.objects.filter(user=request.user).select_related("review")

    if request.method == "POST" and "review_app_id" in request.POST:
        app = get_object_or_404(Application, pk=request.POST["review_app_id"], user=request.user)
        if app.status != Application.Status.COMPLETED:
            messages.error(request, "Отзыв можно оставить только после завершения обучения.")
        elif hasattr(app, "review"):
            messages.warning(request, "Отзыв по этой заявке уже оставлен.")
        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.application = app
                review.save()
                messages.success(request, "Спасибо за отзыв!")
                return redirect("portal:application_list")
            messages.error(request, "Проверьте поля отзыва.")

    return render(request, "portal/applications/list.html", {"applications": applications})


@login_required_custom
def application_create_view(request):
    """Формирование новой заявки."""
    form = ApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.save()
        messages.success(request, "Заявка отправлена на рассмотрение администратору.")
        return redirect("portal:application_list")

    return render(request, "portal/applications/create.html", {"form": form})


def admin_login_view(request):
    form = AdminLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if (
            form.cleaned_data["login"] == ADMIN_LOGIN
            and form.cleaned_data["password"] == ADMIN_PASSWORD
        ):
            request.session["is_portal_admin"] = True
            messages.success(request, "Добро пожаловать в панель администратора.")
            return redirect("portal:admin_dashboard")
        messages.error(request, "Неверный логин или пароль администратора.")

    return render(request, "portal/admin/login.html", {"form": form})


def admin_logout_view(request):
    request.session.pop("is_portal_admin", None)
    messages.info(request, "Вы вышли из панели администратора.")
    return redirect("portal:admin_login")


@admin_session_required
def admin_dashboard_view(request):
    """Панель администратора: все заявки, фильтрация, пагинация."""
    qs = Application.objects.select_related("user").all()

    status_filter = request.GET.get("status", "")
    search = request.GET.get("q", "").strip()
    if status_filter:
        qs = qs.filter(status=status_filter)
    if search:
        qs = qs.filter(
            Q(course_name__icontains=search)
            | Q(user__username__icontains=search)
            | Q(user__full_name__icontains=search)
        )

    paginator = Paginator(qs, 10)
    page = paginator.get_page(request.GET.get("page"))

    if request.method == "POST" and "app_id" in request.POST:
        app = get_object_or_404(Application, pk=request.POST["app_id"])
        status_form = AdminStatusForm(request.POST)
        if status_form.is_valid():
            app.status = status_form.cleaned_data["status"]
            app.save()
            messages.success(request, f"Статус заявки #{app.pk} обновлён.")

    return render(
        request,
        "portal/admin/dashboard.html",
        {
            "page_obj": page,
            "status_filter": status_filter,
            "search": search,
            "status_form": AdminStatusForm(),
        },
    )
