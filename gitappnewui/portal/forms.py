"""
Формы страниц регистрации, авторизации, заявок и отзывов.
Тексты кнопок и списки — из exam_config.py.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from exam_config import COURSE_CHOICES

from .models import Application, Review, User
from .validators import (
    validate_full_name,
    validate_login,
    validate_password,
    validate_phone,
)


def _fc(**extra):
    """Класс form-control для Bootstrap."""
    attrs = {"class": "form-control"}
    attrs.update(extra)
    return attrs


class RegistrationForm(forms.ModelForm):
    """Страница регистрации — все поля обязательны."""

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs=_fc(placeholder="Минимум 8 символов")),
    )

    class Meta:
        model = User
        # password НЕ в fields — иначе в БД может попасть незахешированный пароль
        fields = ["username", "full_name", "phone", "email"]
        labels = {
            "username": "Логин",
            "email": "Электронная почта",
        }
        widgets = {
            "username": forms.TextInput(attrs=_fc(placeholder="Латиница и цифры, от 6 символов")),
            "full_name": forms.TextInput(attrs=_fc(placeholder="Иванов Иван Иванович")),
            "phone": forms.TextInput(attrs=_fc(placeholder="8(999)123-45-67")),
            "email": forms.EmailInput(attrs=_fc(placeholder="user@example.com")),
        }

    def clean_username(self):
        login = self.cleaned_data["username"].strip()
        validate_login(login)
        if User.objects.filter(username__iexact=login).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует.")
        return login

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean_full_name(self):
        validate_full_name(self.cleaned_data["full_name"])
        return self.cleaned_data["full_name"]

    def clean_phone(self):
        validate_phone(self.cleaned_data["phone"])
        return self.cleaned_data["phone"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Страница авторизации с сообщениями об ошибках."""

    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs=_fc()))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs=_fc()))

    error_messages = {
        "invalid_login": "Неверный логин или пароль.",
        "inactive": "Учётная запись отключена.",
    }

    def clean_username(self):
        return self.cleaned_data.get("username", "").strip()


class ApplicationForm(forms.ModelForm):
    """Формирование заявки на обучение."""

    course_name = forms.ChoiceField(
        label="Наименование курса",
        choices=[(c, c) for c in COURSE_CHOICES],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    start_date = forms.DateField(
        label="Желаемая дата начала обучения",
        widget=forms.DateInput(
            attrs=_fc(type="text", placeholder="ДД.ММ.ГГГГ"),
            format="%d.%m.%Y",
        ),
        input_formats=["%d.%m.%Y", "%Y-%m-%d"],
    )
    payment_method = forms.ChoiceField(
        label="Способ оплаты",
        choices=Application.PaymentMethod.choices,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Application
        fields = ["course_name", "start_date", "payment_method"]


class ReviewForm(forms.ModelForm):
    """Отзыв после завершения обучения."""

    class Meta:
        model = Review
        fields = ["text", "rating"]
        labels = {
            "text": "Ваш отзыв",
            "rating": "Оценка (1–5)",
        }
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Опишите качество услуг"}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }


class AdminLoginForm(forms.Form):
    """Вход в панель администратора (отдельные учётные данные из задания)."""

    login = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs=_fc(placeholder="Admin")),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs=_fc(placeholder="KorokNET")),
    )

    def clean_login(self):
        return self.cleaned_data["login"].strip()

    def clean_password(self):
        return self.cleaned_data["password"].strip()


class AdminStatusForm(forms.Form):
    """Смена статуса заявки администратором."""

    status = forms.ChoiceField(label="Новый статус")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            (Application.Status.IN_PROGRESS, Application.Status.IN_PROGRESS.label),
            (Application.Status.COMPLETED, Application.Status.COMPLETED.label),
        ]
