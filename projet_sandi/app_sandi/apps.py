from django.apps import AppConfig


class AppSandiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_sandi'

    def ready(self):
        import app_sandi.views.signals
