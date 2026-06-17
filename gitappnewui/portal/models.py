"""
Модели БД — все поля используются в интерфейсе (критерий Б2Д1).
При новом задании: добавьте/измените поля здесь и сделайте makemigrations + migrate.

Важно: choices задавайте здесь (TextChoices), а не импортом из exam_config —
иначе Django будет ругаться на несовпадение с миграциями.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь портала: логин + доп. поля из задания."""

    full_name = models.CharField("ФИО", max_length=200)
    phone = models.CharField("Телефон", max_length=20)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username


class Application(models.Model):
    """Заявка на обучение."""

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Наличными"
        PHONE = "phone", "Переводом по номеру телефона"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "Идет обучение"
        COMPLETED = "completed", "Обучение завершено"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Пользователь",
    )
    course_name = models.CharField("Наименование курса", max_length=255)
    start_date = models.DateField("Желаемая дата начала обучения")
    payment_method = models.CharField(
        "Способ оплаты",
        max_length=20,
        choices=PaymentMethod.choices,
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.course_name} — {self.user.username}"

    def get_payment_display_ru(self) -> str:
        return self.get_payment_method_display()

    def get_status_display_ru(self) -> str:
        return self.get_status_display()


class Review(models.Model):
    """Отзыв о качестве образовательных услуг (после завершения обучения)."""

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="Заявка",
    )
    text = models.TextField("Текст отзыва")
    rating = models.PositiveSmallIntegerField("Оценка", default=5)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        return f"Отзыв к заявке #{self.application_id}"
