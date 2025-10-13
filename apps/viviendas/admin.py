from django.contrib import admin
from django import forms
from django.utils.html import format_html
from utils.storages.r2_storage import upload_to_r2
from .models import TipoVivienda, Vivienda, ViviendaImagen

class ViviendaImagenInline(admin.TabularInline):
    model = ViviendaImagen
    extra = 5  
    max_num = 5
    readonly_fields = ('fecha_registro',)

class ViviendaAdminForm(forms.ModelForm):
    portada_file = forms.FileField(required=False, label="Portada")

    class Meta:
        model = Vivienda
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        portada_file = self.cleaned_data.get("portada_file")
        if portada_file:
            instance.portada_url = upload_to_r2(
                portada_file,
                filename=f"vivienda_portada_{instance.id_vivienda}_{portada_file.name}",
                content_type=portada_file.content_type
            )

        if commit:
            instance.save()
        return instance

@admin.register(TipoVivienda)
class TipoViviendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_registro')
    search_fields = ('nombre',)
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')

@admin.register(Vivienda)
class ViviendaAdmin(admin.ModelAdmin):
    form = ViviendaAdminForm
    list_display = ('nombre','miniatura_portada', 'tipo', 'departamento', 'estado', 'precio', 'permite_financiamiento','comprador', 'fecha_registro')
    list_filter = ('estado', 'tipo', 'departamento', 'permite_financiamiento','comprador')
    search_fields = ('nombre',)
    readonly_fields = ('fecha_registro', 'fecha_actualizacion', 'portada_url', 'miniatura_portada')
    inlines = [ViviendaImagenInline]

    fieldsets = (
        ('Información General', {
            'fields': (
                'nombre', 'tipo', 'departamento', 'descripcion', 
                'precio', 'permite_financiamiento',
                'portada_url', 'portada_file', 'estado','comprador', 'latitude', 'longitude'
            )
        }),
        ('Tiempos de Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def miniatura_portada(self, obj):
        if obj.portada_url:
            return format_html('<img src="{}" style="width: 80px; height:auto;" />', obj.portada_url)
        return "-"
    miniatura_portada.short_description = "Portada"
