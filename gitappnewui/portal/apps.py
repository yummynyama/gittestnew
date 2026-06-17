from django.apps import AppConfig


class PortalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "portal"
    verbose_name = "Портал"

    def ready(self):
        from config.py314_patch import apply

        apply()
