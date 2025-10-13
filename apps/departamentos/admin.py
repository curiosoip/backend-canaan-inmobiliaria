from django.contrib import admin
from .models import Departamento

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'latitude', 'longitude',
        'total_viviendas', 'total_urbanizaciones', 'total_tramites',
        'fecha_registro'
    )
    search_fields = ('nombre',)
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    fieldsets = (
        ('Información del Departamento', {
            'fields': ('nombre', 'latitude', 'longitude')
        }),
        ('Tiempos del Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def total_viviendas(self, obj):
        return obj.viviendas.count()
    total_viviendas.short_description = "Total Viviendas"

    def total_urbanizaciones(self, obj):
        return obj.urbanizaciones.count()
    total_urbanizaciones.short_description = "Total Urbanizaciones"

    def total_tramites(self, obj):
        return obj.tramites.count()
    total_tramites.short_description = "Total Trámites"
