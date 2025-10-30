from django.db import models
import uuid
from decimal import Decimal
from apps.usuarios.models import Usuario
from apps.urbanizaciones.models import Lote
from apps.viviendas.models import Vivienda


class Venta(models.Model):
    TIPO_VENTA = (
        ('CONTADO', 'Venta al Contado'),
        ('CREDITO', 'Venta a Crédito'),
        ('FINANCIAMIENTO', 'Venta con Financiamiento Mixto'),
    )

    id_venta = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas')
    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas')
    vivienda = models.ForeignKey(Vivienda, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas')

    tipo_venta = models.CharField(max_length=20, choices=TIPO_VENTA)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    monto_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saldo_restante = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_cuotas = models.PositiveIntegerField(default=0)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Tasa de interés anual (%)")

    banco_monto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    empresa_monto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    estado = models.CharField(max_length=20, default='PENDIENTE')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        objetivo = self.lote.nombre if self.lote else (self.vivienda.nombre if self.vivienda else "Sin bien")
        return f"{self.usuario.username} - {objetivo} ({self.tipo_venta})"

    def calcular_saldo(self):
        pagos_realizados = sum(p.monto for p in self.pagos.all())
        self.saldo_restante = Decimal(self.monto_total) - Decimal(pagos_realizados)
        self.save(update_fields=['saldo_restante'])

    class Meta:
        db_table = 'venta'
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha_venta"]
