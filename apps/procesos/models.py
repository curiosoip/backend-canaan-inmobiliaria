from django.db import models
import uuid
from apps.usuarios.models import Usuario  
from apps.urbanizaciones.models import Lote
from apps.viviendas.models import Vivienda  

class ProcesoInterno(models.Model):
    id_proceso_interno = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    responsables = models.ManyToManyField(
        Usuario,
        blank=True,
        related_name="procesos_internos"
    )
    
    class Meta:
        db_table = "proceso_interno"
        verbose_name = "Proceso Interno"
        verbose_name_plural = "Procesos Internos"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.titulo}"

class Proceso(models.Model):
    id_proceso = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proceso_interno = models.ForeignKey(
        ProcesoInterno,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="procesos"
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name="procesos", null=True, blank=True)
    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True, related_name="procesos")
    vivienda = models.ForeignKey(Vivienda, on_delete=models.SET_NULL, null=True, blank=True, related_name="procesos")
    
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=50, default="PENDIENTE")  

    requisitos = models.JSONField(blank=True, null=True, help_text="Listado de requisitos y documentos requeridos")
    documentos = models.JSONField(blank=True, null=True, help_text="Archivos subidos por el usuario, referenciados por tipo y nombre")
    observaciones = models.TextField(blank=True, null=True, help_text="Notas adicionales del proceso")

    class Meta:
        db_table = "proceso"
        verbose_name = "Proceso"
        verbose_name_plural = "Procesos"
        ordering = ["-fecha_solicitud"]

    def __str__(self):
        return f"{self.proceso_interno.titulo if self.proceso_interno else self.titulo}"


