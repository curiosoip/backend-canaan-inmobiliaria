# admin.py
from django.contrib import admin
from .models import Mensaje

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'numero_whatsapp', 'correo', 'leido', 'fecha_creacion')
    list_filter = ('leido', 'fecha_creacion')
    search_fields = ('nombre_completo', 'correo', 'numero_whatsapp', 'mensaje')
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)
