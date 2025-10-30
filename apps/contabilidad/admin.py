from django.contrib import admin
from .models import CuentaContable, TransaccionContable, Comprobante

# Registro de cuentas contables
@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo', 'nivel', 'padre', 'fecha_registro')
    search_fields = ('codigo', 'nombre', 'tipo')
    list_filter = ('tipo', 'nivel')
    ordering = ('codigo',)


# Registro de transacciones contables
@admin.register(TransaccionContable)
class TransaccionContableAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descripcion', 'monto_total', 'fecha_transaccion', 'estado', 'usuario', 'urbanizacion')
    search_fields = ('descripcion', 'tipo', 'estado')
    list_filter = ('tipo', 'estado', 'fecha_transaccion')
    ordering = ('-fecha_transaccion',)


# Registro de comprobantes
@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'transaccion', 'fecha_emision', 'archivo_url')
    search_fields = ('numero', 'tipo', 'transaccion__descripcion')
    list_filter = ('tipo', 'fecha_emision')
    ordering = ('-fecha_emision',)
