from django.contrib import admin
from .models import ProcesoInterno, Proceso

@admin.register(ProcesoInterno)
class ProcesoInternoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha_registro", "fecha_actualizacion")
    search_fields = ("titulo",)
    list_filter = ("fecha_registro",)
    filter_horizontal = ("responsables",)  # Para ManyToManyField sin widgets extra
    ordering = ("-fecha_registro",)


@admin.register(Proceso)
class ProcesoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "proceso_interno",
        "usuario",
        "lote",
        "vivienda",
        "estado",
        "fecha_solicitud",
        "fecha_actualizacion",
    )
    search_fields = ("titulo", "descripcion")
    list_filter = ("estado", "fecha_solicitud")
    ordering = ("-fecha_solicitud",)
    raw_id_fields = ("proceso_interno", "usuario", "lote", "vivienda")  # Evita widgets de selección grandes
