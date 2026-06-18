# Django DEMO Cheat Sheet

## Создание модели

```python
from django.db import models

class User(models.Model):
    pass
```

---

# Самые нужные поля

## Текст

```python
name = models.CharField(max_length=100)
```

Для:

* ФИО
* Логина
* Телефона
* Паспорта

---

## Большой текст

```python
comment = models.TextField()
```

Для:

* отзывов
* комментариев
* описаний

---

## Число

```python
age = models.IntegerField()
```

---

## Деньги

```python
price = models.DecimalField(
    max_digits=10,
    decimal_places=2
)
```

---

## Email

```python
email = models.EmailField()
```

---

## Дата

```python
birth_date = models.DateField()
```

---

## Дата и время

```python
created_at = models.DateTimeField()
```

---

## Автоматическая дата создания

```python
created_at = models.DateTimeField(
    auto_now_add=True
)
```

---

## Автоматическая дата изменения

```python
updated_at = models.DateTimeField(
    auto_now=True
)
```

---

## Сайт

```python
website = models.URLField()
```

---

## Файл

```python
document = models.FileField(
    upload_to="documents/"
)
```

---

## Изображение

```python
avatar = models.ImageField(
    upload_to="avatars/"
)
```

```bash
pip install pillow
```

---

# Полезные параметры

## Красивое название

```python
passport = models.CharField(
    "Паспорт",
    max_length=20
)
```

---

## Можно оставить пустым

```python
comment = models.TextField(
    blank=True
)
```

---

## Можно хранить NULL

```python
comment = models.TextField(
    null=True,
    blank=True
)
```

---

## Значение по умолчанию

```python
status = models.CharField(
    max_length=20,
    default="Новая"
)
```

---

## Только уникальные значения

```python
passport = models.CharField(
    max_length=20,
    unique=True
)
```

---

## Индекс для быстрого поиска

```python
phone = models.CharField(
    max_length=20,
    db_index=True
)
```

---

# Связи между таблицами

## Один ко многим

Один пользователь → много заявок

```python
user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
)
```

---

## Один к одному

```python
user = models.OneToOneField(
    User,
    on_delete=models.CASCADE
)
```

---

## Многие ко многим

```python
courses = models.ManyToManyField(
    Course
)
```

---

# Choices (выпадающий список)

```python
class Status(models.TextChoices):
    NEW = "new", "Новая"
    DONE = "done", "Завершена"

status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.NEW
)
```

---

# Переименование поля

Было:

```python
age = models.IntegerField()
```

Стало:

```python
user_age = models.IntegerField()
```

После:

```bash
python manage.py makemigrations
```

Django обычно спросит:

```text
Was age renamed to user_age?
```

Отвечаем:

```text
y
```

Тогда данные сохранятся.

---

# Добавление нового поля

Было:

```python
age = models.IntegerField()
```

Стало:

```python
age = models.IntegerField()
age2 = models.IntegerField(
    null=True,
    blank=True
)
```

Получится два столбца:

| age | age2 |
| --- | ---- |

Данные сохранятся.

---

# Изменение модели

После любого изменения:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Если Django ругается на default

Ошибка:

```text
It is impossible to add a non-nullable field...
```

Означает:

> В таблице уже есть данные, а ты добавил новое обязательное поле.

Обычно можно выбрать:

```text
1
```

и написать:

```python
''
```

Все старые данные сохранятся.

---

# Полезные команды

Создать миграции:

```bash
python manage.py makemigrations
```

Применить миграции:

```bash
python manage.py migrate
```

Посмотреть миграции:

```bash
python manage.py showmigrations
```

Создать администратора:

```bash
python manage.py createsuperuser
```

Запустить сервер:

```bash
python manage.py runserver
```

Открыть Django Shell:

```bash
python manage.py shell
```

---

# Лайфхаки для демо

Практически всегда пригодятся:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

---

Для телефона:

```python
phone = models.CharField(
    max_length=20,
    unique=True
)
```

---

Для статуса:

```python
status = models.CharField(
    max_length=20,
    default="Новая"
)
```

---

Для комментариев:

```python
comment = models.TextField(
    blank=True
)
```

---

# Золотое правило

Изменил models.py?

```bash
python manage.py makemigrations
python manage.py migrate
```

Сделал миграции → запускай проект.
