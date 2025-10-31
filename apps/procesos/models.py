from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Proceso(models.Model):
    nombre = models.CharField(max_length=200)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'rol__nombre': 'CLIENTE'},
        on_delete=models.CASCADE,
        related_name='procesos',
        help_text="Usuario que actúa como cliente"
    )
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    encargado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'rol__nombre__in': ['ADMINISTRATIVO', 'ARQUITECTO', 'TOPOGRAFO']},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='procesos_encargados',
        help_text="Empleado responsable de supervisar todo el proceso"
    )
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.username}"


class Tarea(models.Model):
    """
    Una tarea es una actividad concreta dentro de un proceso.
    """
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En progreso'),
        ('COMPLETADA', 'Completada'),
        ('ATRASADA', 'Atrasada'),
    ]

    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'rol__nombre__in': ['ADMINISTRATIVO', 'ARQUITECTO', 'TOPOGRAFO']},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas_asignadas'
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_limite = models.DateTimeField(blank=True, null=True)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    prioridad = models.PositiveIntegerField(default=1, help_text="1 = baja, 5 = alta")

    def tiempo_restante(self):
        """Devuelve el tiempo restante en horas para completar la tarea."""
        if self.fecha_limite and self.fecha_inicio:
            delta = self.fecha_limite - self.fecha_inicio
            return delta.total_seconds() / 3600
        return None

    def atrasada(self):
        """Indica si la tarea está atrasada."""
        if self.estado != 'COMPLETADA' and self.fecha_limite:
            return timezone.now() > self.fecha_limite
        return False

    def __str__(self):
        return
