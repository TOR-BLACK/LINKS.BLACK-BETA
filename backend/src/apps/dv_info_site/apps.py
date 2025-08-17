from django.apps import AppConfig


class DvInfoSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dv_info_site'
    verbose_name = 'Инфосайт localhost'

    def ready(self):
        from .signals import connect_signals_to_all_models
        connect_signals_to_all_models()