from django.contrib import admin
from .models import Venta
from apps.cuotas.models import Cuota
from apps.pagos.models import Pago

class PagoInline(admin.TabularInline):
    model = Pago
    extra = 0
    readonly_fields = ('fecha_pago',)
    fields = ('usuario', 'tipo', 'monto', 'cuota', 'fecha_pago')
    show_change_link = True

class CuotaInline(admin.TabularInline):
    model = Cuota
    extra = 0
    readonly_fields = ('fecha_pago', 'pagada')
    fields = ('numero', 'monto', 'fecha_vencimiento', 'pagada', 'fecha_pago')
    show_change_link = True

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_objetivo', 'tipo_venta', 'monto_total', 'monto_inicial', 'saldo_restante', 'total_cuotas', 'estado', 'fecha_venta')
    search_fields = ('usuario__username', 'lote__nombre', 'vivienda__nombre', 'tipo_venta')
    list_filter = ('tipo_venta', 'estado', 'fecha_venta')
    ordering = ('-fecha_venta',)
    inlines = [CuotaInline, PagoInline]

    def get_objetivo(self, obj):
        return obj.lote.nombre if obj.lote else (obj.vivienda.nombre if obj.vivienda else "Sin bien")
    get_objetivo.short_description = 'Bien'
