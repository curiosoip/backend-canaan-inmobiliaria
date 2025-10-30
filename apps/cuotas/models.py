from django.db import models
import uuid
from apps.ventas.models import Venta

class Cuota(models.Model):
    id_cuota = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='cuotas')
    numero = models.PositiveIntegerField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_vencimiento = models.DateField()
    pagada = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'cuota'
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"
        ordering = ["numero"]

    def __str__(self):
        return f"Cuota {self.numero} - {self.venta}"

