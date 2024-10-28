
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    numero_control = models.CharField(max_length=10, unique=True)  # Campo para el número de control

    def __str__(self):
        return self.username  # Puedes devolver otro campo como numero_control si lo prefieres


class Examen(models.Model):
    fecha = models.DateTimeField()  # Almacena la fecha y hora del examen
    cupo = models.PositiveIntegerField(default=30)
    costo = models.DecimalField(max_digits=6, decimal_places=2, default=500)  # Costo del examen

    def save(self, *args, **kwargs):
        # Si 'fecha' no se proporciona, se establece para dentro de una semana a la misma hora actual
        if not self.fecha:
            self.fecha = timezone.now() + timedelta(weeks=1)
        super().save(*args, **kwargs)

    @property
    def cupo_disponible(self):
        solicitudes = SolicitudExamen.objects.filter(examen=self).count()
        return self.cupo - solicitudes

    def __str__(self):
        return f'{self.fecha}'


class SolicitudExamen(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    estado_pago = models.BooleanField(default=False)  # True si el pago está confirmado
    calificacion = models.IntegerField(null=True, blank=True, default=0)  # Calificación del alumno
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'examen')

    @property
    def aprobado(self):
        """Retorna 'Aprobado' si la calificación es >= 70, si no, 'Reprobado'."""
        if self.calificacion is not None:
            return 'Aprobado' if self.calificacion >= 70 else 'Reprobado'
        return 'Sin calificación'
    
    
