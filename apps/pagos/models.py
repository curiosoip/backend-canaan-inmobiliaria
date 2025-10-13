from django.db import models
import uuid
from apps.usuarios.models import Usuario
from apps.urbanizaciones.models import Lote
from apps.viviendas.models import Vivienda

class Pago(models.Model):
    CATEGORIA_PAGO = (
        ('DIRECTO', 'Pago Directo'),
        ('CUOTA', 'Cuotas'),
    )
    TIPO_PAGO = (
        ('Efectivo', 'Efectivo'),
        ('QR', 'Pago QR'),
    )

    id_pago = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos')
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='pagos', null=True, blank=True)
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, related_name='pagos', null=True, blank=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_PAGO)
    tipo = models.CharField(max_length=15, choices=TIPO_PAGO)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    cuota_numero = models.IntegerField(blank=True, null=True)
    total_cuotas = models.IntegerField(blank=True, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.lote and not self.vivienda:
            raise ValidationError("El pago debe estar asociado a un lote o a una vivienda.")
        if self.lote and self.vivienda:
            raise ValidationError("El pago no puede estar asociado a un lote y vivienda al mismo tiempo.")

    def __str__(self):
        objetivo = self.lote.nombre if self.lote else (self.vivienda.nombre if self.vivienda else "Sin objetivo")
        return f"{self.usuario.username} - {objetivo} ({self.tipo})"

    class Meta:
        db_table = 'pago'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["fecha_registro"]
