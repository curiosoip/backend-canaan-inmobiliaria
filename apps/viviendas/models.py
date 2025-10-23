from django.db import models
import uuid
from apps.departamentos.models import Departamento
from apps.usuarios.models import Usuario

class TipoVivienda(models.Model):
    id_tipo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "tipo_vivienda"
        verbose_name = "Tipo de Vivienda"
        verbose_name_plural = "Tipos de Vivienda"
        ordering = ["nombre"]

class CaracteristicaVivienda(models.Model):
    TIPO_CARACTERISTICA = (
        ('INTERNA', 'Interna'),
        ('EXTERNA', 'Externa'),
    )

    id_caracteristica = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vivienda = models.ForeignKey('Vivienda', on_delete=models.CASCADE, related_name='caracteristicas')
    tipo = models.CharField(max_length=10, choices=TIPO_CARACTERISTICA)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    cantidad=models.IntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

    class Meta:
        db_table = "caracteristica_vivienda"
        verbose_name = "Característica de Vivienda"
        verbose_name_plural = "Características de Viviendas"
        ordering = ["tipo", "nombre"]

class Vivienda(models.Model):
    ESTADO_VIVIENDA = (
        ('DISPONIBLE', 'Disponible'),
        ('EN_CREDITO', 'En Crédito'),
        ('OCUPADO', 'Ocupado'),
    )

    id_vivienda = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='viviendas')
    tipo = models.ForeignKey(TipoVivienda, on_delete=models.SET_NULL, null=True, blank=True, related_name='viviendas')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    portada_url = models.URLField(blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADO_VIVIENDA, default='DISPONIBLE')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    permite_financiamiento = models.BooleanField(default=False)
    comprador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='viviendas_compradas')
    superficie = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Superficie construida en m²")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo.nombre if self.tipo else 'Sin tipo'})"

    class Meta:
        db_table = "vivienda"
        verbose_name = "Vivienda"
        verbose_name_plural = "Viviendas"
        ordering = ["nombre"]

class ViviendaImagen(models.Model):
    id_imagen = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, related_name='galeria')
    imagen_url = models.URLField(blank=True,null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen de {self.vivienda.nombre}"

    class Meta:
        db_table = "vivienda_imagen"
        verbose_name = "Imagen de Vivienda"
        verbose_name_plural = "Galería de Viviendas"
        ordering = ["fecha_registro"]
