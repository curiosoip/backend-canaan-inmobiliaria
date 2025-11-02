# apps/redcors/models.py
from django.db import models
import uuid

class RedCORS(models.Model):
    TIPO_SERVICIO_CHOICES = [
        ('conexion', 'Conexión de Red'),
        ('mantenimiento', 'Mantenimiento de Infraestructura'),
        ('optimización', 'Optimización de Red'),
        ('seguridad', 'Seguridad y Monitoreo'),
        ('soporte', 'Soporte Técnico'),
    ]

    id_redcors = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_proyecto = models.CharField(max_length=150, help_text="Nombre del proyecto o área donde se realiza el servicio")
    tipo_servicio = models.CharField(max_length=50, choices=TIPO_SERVICIO_CHOICES)
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del servicio realizado")
    proveedor = models.CharField(max_length=150, blank=True, help_text="Proveedor o empresa encargada del servicio")
    observaciones = models.TextField(blank=True, help_text="Notas u observaciones adicionales")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Red CORS"
        verbose_name_plural = "Redes CORS"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_proyecto} - {self.get_tipo_servicio_display()}"
