# apps.py
from django.apps import AppConfig

class TuAplicacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplicacion'

    def ready(self):
        import aplicacion.signals  # Asegúrate de que el módulo signals se importe
