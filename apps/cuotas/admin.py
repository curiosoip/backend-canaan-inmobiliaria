from django.contrib import admin
from .models import Cuota

@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'venta', 'monto', 'fecha_vencimiento', 'pagada', 'fecha_pago')
    search_fields = ('venta__id_venta',)
    list_filter = ('pagada', 'fecha_vencimiento')
    ordering = ('venta', 'numero')
