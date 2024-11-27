# facade.py
from .models import Examen, SolicitudExamen

class ExamenFacade:
    @staticmethod
    def crear_examen(fecha, cupo, costo):
        examen = Examen(fecha=fecha, cupo=cupo, costo=costo)
        examen.save()
        return examen

    @staticmethod
    def solicitar_examen(usuario, examen):
        solicitud = SolicitudExamen(usuario=usuario, examen=examen)
        solicitud.save()
        return solicitud

    @staticmethod
    def obtener_examenes_disponibles():
        return Examen.objects.filter(cupo__gt=0)  # Retorna solo exámenes con cupo disponible

    @staticmethod
    def obtener_solicitudes_por_usuario(usuario):
        return SolicitudExamen.objects.filter(usuario=usuario)
