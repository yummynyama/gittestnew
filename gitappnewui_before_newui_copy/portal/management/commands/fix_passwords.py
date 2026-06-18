"""
Перехешировать пароли пользователей, если они были сохранены до исправления формы.
Запуск: python manage.py fix_passwords --username student1 --password password1
"""
from django.core.management.base import BaseCommand

from portal.models import User


class Command(BaseCommand):
    help = "Установить пароль пользователю (если вход не работает после регистрации)"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Пароль для «{username}» обновлён."))
