from django.db import models
import uuid
from apps.usuarios.models import Usuario
from apps.cuotas.models import Cuota
from apps.ventas.models import Venta


class Pago(models.Model):
    TIPO_PAGO = (
        ('Efectivo', 'Efectivo'),
        ('QR', 'Pago QR'),
        ('Transferencia', 'Transferencia'),
    )

    id_pago = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos')
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos', null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=TIPO_PAGO)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    cuota = models.ForeignKey(Cuota, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.cuota and self.cuota.venta != self.venta:
            raise ValidationError("La cuota no pertenece a la venta seleccionada.")

    def __str__(self):
        return f"{self.usuario.username} - {self.venta} ({self.tipo})"

    class Meta:
        db_table = 'pago'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["-fecha_registro"]
