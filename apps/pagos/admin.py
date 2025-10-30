from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'venta', 'cuota', 'tipo', 'monto', 'fecha_pago')
    search_fields = ('usuario__username', 'venta__id_venta', 'cuota__id')
    list_filter = ('tipo', 'fecha_pago')
    ordering = ('-fecha_pago',)
