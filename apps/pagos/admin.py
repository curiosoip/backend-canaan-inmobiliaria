from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'get_objetivo',
        'categoria', 
        'tipo', 
        'monto', 
        'cuota_numero', 
        'total_cuotas', 
        'fecha_pago',
        'fecha_registro',
    )
    list_filter = ('categoria', 'tipo', 'fecha_pago')
    search_fields = ('usuario__username', 'lote__nombre', 'vivienda__nombre')
    readonly_fields = ('fecha_pago', 'fecha_registro', 'fecha_actualizacion')
    fieldsets = (
        ('Información del Pago', {
            'fields': ('usuario', 'lote', 'vivienda', 'categoria', 'tipo', 'monto', 'cuota_numero', 'total_cuotas')
        }),
        ('Tiempos del Registro', {
            'fields': ('fecha_pago', 'fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_objetivo(self, obj):
        return obj.lote.nombre if obj.lote else (obj.vivienda.nombre if obj.vivienda else '-')
    get_objetivo.short_description = 'Lote/Vivienda'
