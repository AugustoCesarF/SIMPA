from django.apps import AppConfig


class ComunidadeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "comunidade"
    verbose_name = "Comunidade e Integrações"

    def ready(self):
        import comunidade.signals  # noqa
