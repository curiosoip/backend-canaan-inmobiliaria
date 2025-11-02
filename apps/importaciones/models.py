from django.db import models
import uuid

class Importacion(models.Model):
    TIPO_IMPORTACION_CHOICES = [
        ('materiales', 'Materiales de construcción'),
        ('maquinaria', 'Maquinaria y equipos'),
        ('equipos_hvac', 'Equipos HVAC y eléctricos'),
        ('acabados', 'Acabados e interiorismo'),
        ('herramientas', 'Herramientas y suministros menores'),
        ('otros', 'Otros'),
    ]

    id_importacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    tipo_importacion = models.CharField(
        max_length=50,
        choices=TIPO_IMPORTACION_CHOICES,
        blank=True,
        null=True,
        help_text="Seleccione el tipo de importación"
    )
    servicios_asociados = models.TextField(blank=True, null=True)
    proveedores = models.TextField(blank=True, null=True)
    proceso_trabajo = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Importación"
        verbose_name_plural = "Importaciones"
        ordering = ['-fecha_registro']

    def __str__(self):
        return self.nombre
