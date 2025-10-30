from django.db import models
import uuid
from decimal import Decimal
from apps.usuarios.models import Usuario
from apps.urbanizaciones.models import Urbanizacion



class CuentaContable(models.Model):
    TIPO_CUENTA = (
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
        ('ACTIVO', 'Activo'),
        ('PASIVO', 'Pasivo'),
        ('PATRIMONIO', 'Patrimonio'),
    )

    id_cuenta = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CUENTA)
    descripcion = models.TextField(blank=True, null=True)
    nivel = models.PositiveIntegerField(default=1) 
    padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcuentas')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cuenta_contable'
        verbose_name = "Cuenta Contable"
        verbose_name_plural = "Cuentas Contables"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    

class TransaccionContable(models.Model):
    TIPO_TRANSACCION = (
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    )

    id_transaccion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones')
    tipo = models.CharField(max_length=10, choices=TIPO_TRANSACCION)
    descripcion = models.TextField(blank=True, null=True)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    urbanizacion = models.ForeignKey(Urbanizacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones')

    venta = models.ForeignKey('ventas.Venta', on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones')
    pago = models.ForeignKey('pagos.Pago', on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones')

    estado = models.CharField(max_length=20, default='REGISTRADO')

    def __str__(self):
        return f"{self.tipo} - {self.descripcion or 'Sin descripción'} ({self.monto_total})"

    class Meta:
        db_table = 'transaccion_contable'
        verbose_name = "Transacción Contable"
        verbose_name_plural = "Transacciones Contables"
        ordering = ['-fecha_transaccion']


class Comprobante(models.Model):
    TIPO_COMPROBANTE = (
        ('FACTURA', 'Factura'),
        ('RECIBO', 'Recibo'),
        ('INTERNO', 'Comprobante Interno'),
    )

    id_comprobante = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_COMPROBANTE)
    transaccion = models.ForeignKey(TransaccionContable, on_delete=models.CASCADE, related_name='comprobantes')
    fecha_emision = models.DateField(auto_now_add=True)
    archivo_url = models.URLField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'comprobante'
        verbose_name = "Comprobante Contable"
        verbose_name_plural = "Comprobantes Contables"
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"{self.tipo} #{self.numero}"
