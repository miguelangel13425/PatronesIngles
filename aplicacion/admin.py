from django.contrib import admin
from .models import Examen, SolicitudExamen



# Registra los modelos en el admin
admin.site.register(Examen)
admin.site.register(SolicitudExamen)
