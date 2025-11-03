from django.contrib import admin
from .models import Tramite, Requisito

class RequisitoInline(admin.TabularInline):
    model = Requisito
    extra = 1 
    fields = ('nombre', 'descripcion', 'obligatorio', 'archivo_requerido', 'orden')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    ordering = ('orden',)


@admin.register(Tramite)
class TramiteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'tiempo_estimado', 'activo', 'fecha_registro')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    inlines = [RequisitoInline]
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')

    fieldsets = (
        ('Información del Trámite', {
            'fields': ('departamentos','nombre', 'descripcion', 'costo', 'tiempo_estimado', 'activo')
        }),
        ('Tiempos del Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


