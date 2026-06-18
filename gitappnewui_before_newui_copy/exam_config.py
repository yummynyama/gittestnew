"""
=============================================================================
  ФАЙЛ НАСТРОЙКИ ПОД КОНКРЕТНОЕ ЗАДАНИЕ ЭКЗАМЕНА
  Меняйте значения здесь — остальной код подстроится автоматически.
=============================================================================
"""

# --- Название портала и предметная область ---
SITE_NAME = "Корочки.есть"
SITE_TAGLINE = "Портал записи на курсы дополнительного профессионального образования"
TARGET_AUDIENCE = "специалисты, повышающие квалификацию"

# --- Учётные данные администратора (из задания) ---
ADMIN_LOGIN = "Admin"
ADMIN_PASSWORD = "KorokNET"

# --- Список курсов (выпадающий список на странице заявки, модуль 2) ---
COURSE_CHOICES = [
    "Основы алгоритмизации и программирования",
    "Основы веб-дизайна",
    "Основы проектирования баз данных",
]

# --- Способы оплаты ---
PAYMENT_CHOICES = [
    ("cash", "Наличными"),
    ("phone", "Переводом по номеру телефона"),
]

# --- Статусы заявок ---
APPLICATION_STATUS_NEW = "new"
APPLICATION_STATUS_IN_PROGRESS = "in_progress"
APPLICATION_STATUS_COMPLETED = "completed"

APPLICATION_STATUS_LABELS = {
    APPLICATION_STATUS_NEW: "Новая",
    APPLICATION_STATUS_IN_PROGRESS: "Идет обучение",
    APPLICATION_STATUS_COMPLETED: "Обучение завершено",
}

# Статусы, которые админ может выставить (кроме «Новая» — она по умолчанию)
ADMIN_STATUS_CHOICES = [
    (APPLICATION_STATUS_IN_PROGRESS, APPLICATION_STATUS_LABELS[APPLICATION_STATUS_IN_PROGRESS]),
    (APPLICATION_STATUS_COMPLETED, APPLICATION_STATUS_LABELS[APPLICATION_STATUS_COMPLETED]),
]

# --- Валидация регистрации (регулярки и ограничения) ---
LOGIN_MIN_LENGTH = 6
PASSWORD_MIN_LENGTH = 8
# Логин: латиница и цифры
LOGIN_REGEX = r"^[a-zA-Z0-9]+$"
# ФИО: кириллица и пробелы
FULL_NAME_REGEX = r"^[А-Яа-яЁё\s]+$"
# Телефон: 8(XXX)XXX-XX-XX
PHONE_REGEX = r"^8\(\d{3}\)\d{3}-\d{2}-\d{2}$"

# --- Тексты кнопок и ссылок (подставьте из задания) ---
BTN_CREATE_USER = "Создать пользователя"
BTN_REGISTER = "Зарегистрироваться"
BTN_LOGIN = "Войти"
BTN_SEND_APPLICATION = "Отправить"
BTN_LEAVE_REVIEW = "Оставить отзыв"

LINK_TO_REGISTER = "Еще не зарегистрированы? Регистрация"
LINK_TO_LOGIN = "Уже есть аккаунт? Войти"

# --- Слайдер (модуль 2): интервал смены кадров в мс ---
SLIDER_INTERVAL_MS = 3000
