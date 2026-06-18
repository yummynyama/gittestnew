# Шпаргалка по экзамену — Django + Bootstrap (ГИА 09.02.07)

---

## 0. Без интернета — подготовь заранее дома!

> Всё это делается **до экзамена**, пока есть интернет.

### Django и библиотеки
```bash
pip install -r requirements.txt
```
Установи заранее — на экзамене pip работать не будет.

### Bootstrap локально
1. Скачай Bootstrap 5.3.3 с [getbootstrap.com](https://getbootstrap.com) → Download
2. Положи файлы в проект:
   - `bootstrap.min.css` → `static/css/`
   - `bootstrap.bundle.min.js` → `static/js/`
3. Замени CDN-ссылки в `portal/templates/portal/base.html`:

```html
<!-- БЫЛО (CDN — не работает без интернета) -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<!-- СТАЛО (локально) -->
<link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
<script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
```

---

## 1. Прочитай задание и выпиши на листок

Ответь на 5 вопросов:

1. Как называется система? *(для сайта)*
2. Какие поля при регистрации? *(ФИО, телефон, email — или другие)*
3. Что пользователь создаёт? *(заявка, бронь, заказ...)*
4. Какие поля у этой штуки? *(название, дата, способ оплаты...)*
5. Логин/пароль админа и статусы заявок?

---

## 2. Поменяй названия и тексты — файл `exam_config.py`

Открой `exam_config.py` и замени значения:

```python
SITE_NAME = "Название из задания"
ADMIN_LOGIN = "Логин из задания"
ADMIN_PASSWORD = "Пароль из задания"

COURSE_CHOICES = [
    "Вариант 1 из задания",
    "Вариант 2 из задания",
]

PAYMENT_CHOICES = [
    ("cash", "Наличными"),
    ("card", "Банковской картой"),  # ← если нужно другое
]
```

> ⚠️ После изменения этого файла — перезапусти сервер (`Ctrl+C` → `python manage.py runserver`)

---

## 3. Если нужны другие поля в базе — файл `portal/models.py`

Там три блока:

| Класс | Что содержит |
|---|---|
| `class User` | Поля пользователя при регистрации: ФИО, телефон, email и т.д. |
| `class Application` | Поля заявки: название, дата, способ оплаты, статусы |

**Добавить новое поле** — вставь строчку внутрь класса:
```python
passport = models.CharField("Серия и номер паспорта", max_length=20)
```

**Добавить новый способ оплаты** — в `PaymentMethod`:
```python
class PaymentMethod(models.TextChoices):
    CASH = "cash", "Наличными"
    CARD = "card", "Банковской картой"
    PHONE = "phone", "По телефону"   # ← добавил
```

**Добавить новый статус** — в `Status`:
```python
class Status(models.TextChoices):
    NEW = "new", "Новая"
    WAITING = "waiting", "Ожидает оплаты"   # ← добавил
    COMPLETED = "completed", "Завершена"
```

---

## 4. Обновить базу данных (обязательно после `models.py`)

После любого изменения в `models.py` — выполни в терминале:

```bash
python manage.py makemigrations portal
python manage.py migrate
```

> ⚠️ Если ругается на старые данные — удали `db.sqlite3` и снова запусти `migrate`

---

## 5. Поля на формах — файл `portal/forms.py`

Открой `portal/forms.py`. Если добавил новое поле в модель — добавь его и сюда.

**Добавить поле в форму регистрации** (класс `RegistrationForm`):
```python
fields = ["username", "full_name", "phone", "email", "passport"]  # ↑ добавил
```

**Добавить поле в форму заявки** (класс `ApplicationForm`):
```python
fields = ["course_name", "start_date", "payment_method", "comment"]  # ↑ добавил
```

---

## 6. Тексты на страницах — папка `templates`

В папке `portal/templates/portal/` — HTML-файлы страниц.

Поменяй слова которые видит пользователь: «курс» → «автомобиль», «обучение» → «аренда» и т.д.
Можно использовать `Ctrl+F` для поиска нужного слова.

---

## ✅ Порядок файлов — не перепрыгивай!

```
exam_config.py       →  тексты, списки, логин/пароль админа
        ↓
models.py            →  таблицы и поля базы данных
        ↓
makemigrations + migrate  →  применить изменения БД
        ↓
forms.py             →  поля на формах
        ↓
templates/*.html     →  тексты которые видит пользователь
```
