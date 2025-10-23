from django.db import models
import uuid
from apps.usuarios.models import Usuario
from apps.departamentos.models import Departamento

class Urbanizacion(models.Model):
    id_urbanizacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    portada_url = models.URLField(blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='urbanizaciones')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    planimetria_pdf = models.URLField(blank=True, null=True)
    total_lotes=models.IntegerField(blank=True,null=True,default=0)
    total_manzanas=models.IntegerField(blank=True,null=True,default=0)
    area_total=models.FloatField(blank=True,null=True,default=0.0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'urbanizacion'
        verbose_name = "Urbanizacion"
        verbose_name_plural = "Urbanizaciones"
        ordering = ["nombre"]

class VerticeUrbanizacion(models.Model):
    id_vertices_urbanizacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    urbanizacion = models.ForeignKey('Urbanizacion', on_delete=models.CASCADE, related_name='vertices')
    este_x = models.DecimalField(max_digits=14, decimal_places=6)
    norte_y = models.DecimalField(max_digits=14, decimal_places=6)
    orden = models.CharField(max_length=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vertices_urbanizacion'
        verbose_name = "Vértices de la Urbanización"
        verbose_name_plural = "Vértices de las Urbanizaciones"
        ordering = ['orden']

    def __str__(self):
        return f"V{self.orden} ({self.este_x}, {self.norte_y})"


class Lote(models.Model):
    ESTADO_LOTE = (
        ('DISPONIBLE', 'Disponible'),
        ('EN_CREDITO', 'En Crédito'),
        ('OCUPADO', 'Ocupado'),
    )
    id_lote = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    urbanizacion = models.ForeignKey(Urbanizacion, on_delete=models.CASCADE, related_name='lotes',blank=True,null=True)
    nombre = models.CharField(max_length=50)
    area_m2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    comprador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='lotes_comprados')
    estado = models.CharField(max_length=15, choices=ESTADO_LOTE, default='DISPONIBLE')
    manzana = models.CharField(max_length=1, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.urbanizacion.nombre})"

    
    class Meta:
        db_table = 'lote'
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        ordering = ["nombre"]
