from django.db import models
import uuid
from apps.departamentos.models import Departamento

class Tramite(models.Model):
    id_tramite = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL,blank=True,null=True, related_name='tramites')
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.CharField(max_length=200,blank=True,null=True)
    tiempo_estimado = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tramite'
        verbose_name = "Trámite"
        verbose_name_plural = "Trámites"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Requisito(models.Model):
    id_requisito_tramite = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE, related_name='requisitos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    obligatorio = models.BooleanField(default=True)
    archivo_requerido = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'requisito'
        verbose_name = "Requisito"
        verbose_name_plural = "Requisitos"
        ordering = ["orden"]

    def __str__(self):
        return f"{self.nombre} ({self.tramite.nombre})"
