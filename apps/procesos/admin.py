from django.contrib import admin
from .models import Proceso, Tarea

@admin.register(Proceso)
class ProcesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'encargado', 'fecha_inicio', 'fecha_fin', 'finalizado')
    list_filter = ('finalizado', 'fecha_inicio', 'fecha_fin', 'encargado')
    search_fields = ('nombre', 'cliente__username', 'encargado__username')
    ordering = ('-fecha_inicio',)
    readonly_fields = ('fecha_inicio',)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proceso', 'responsable', 'estado', 'fecha_creacion', 'fecha_inicio', 'fecha_limite', 'fecha_completado', 'prioridad')
    list_filter = ('estado', 'prioridad', 'responsable', 'proceso')
    search_fields = ('titulo', 'proceso__nombre', 'responsable__username')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion',)
