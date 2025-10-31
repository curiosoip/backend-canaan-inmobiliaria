from django.db import models
import uuid

class Servicio(models.Model):
    id_servicio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'servicio'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-fecha_registro']
