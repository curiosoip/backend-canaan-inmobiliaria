from django.db import models
import uuid
from apps.usuarios.models import Usuario  

class Consultoria(models.Model):
    id_consultoria = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    descripcion_general = models.TextField(blank=True, null=True)  
    servicios_especializados = models.TextField(blank=True, null=True)  
    proceso_trabajo = models.TextField(blank=True, null=True)  
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Consultoría"
        verbose_name_plural = "Consultorías"
        ordering = ['-fecha_registro']

    def __str__(self):
        return self.nombre
