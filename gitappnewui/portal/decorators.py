from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def login_required_custom(view_func):
    """Проверка авторизации пользователя портала."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Для доступа необходимо войти в систему.")
            return redirect("portal:login")
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_session_required(view_func):
    """Проверка сессии панели администратора."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_portal_admin"):
            return redirect("portal:admin_login")
        return view_func(request, *args, **kwargs)

    return wrapper
