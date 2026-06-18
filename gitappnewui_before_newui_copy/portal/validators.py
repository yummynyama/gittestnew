"""
Валидаторы полей регистрации.
При смене задания — правьте exam_config.py (регулярки и длины).
"""
import re

from django.core.exceptions import ValidationError

from exam_config import (
    FULL_NAME_REGEX,
    LOGIN_MIN_LENGTH,
    LOGIN_REGEX,
    PASSWORD_MIN_LENGTH,
    PHONE_REGEX,
)


def validate_login(value: str) -> None:
    if len(value) < LOGIN_MIN_LENGTH:
        raise ValidationError(f"Логин должен содержать не менее {LOGIN_MIN_LENGTH} символов.")
    if not re.fullmatch(LOGIN_REGEX, value):
        raise ValidationError("Логин может содержать только латиницу и цифры.")


def validate_password(value: str) -> None:
    if len(value) < PASSWORD_MIN_LENGTH:
        raise ValidationError(f"Пароль должен содержать не менее {PASSWORD_MIN_LENGTH} символов.")


def validate_full_name(value: str) -> None:
    if not re.fullmatch(FULL_NAME_REGEX, value.strip()):
        raise ValidationError("ФИО может содержать только кириллицу и пробелы.")


def validate_phone(value: str) -> None:
    if not re.fullmatch(PHONE_REGEX, value):
        raise ValidationError("Телефон должен быть в формате 8(XXX)XXX-XX-XX.")
