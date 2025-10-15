from django.contrib import admin
from django import forms
from django.utils.html import format_html
from utils.storages.r2_storage import upload_to_r2
from .models import TipoVivienda, Vivienda, ViviendaImagen,CaracteristicaVivienda

class ViviendaImagenForm(forms.ModelForm):
    imagen_file = forms.FileField(required=False, label="Subir imagen")

    class Meta:
        model = ViviendaImagen
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        imagen_file = self.cleaned_data.get("imagen_file")
        if imagen_file:
            # Subimos la imagen y guardamos la URL
            instance.imagen_url = upload_to_r2(
                imagen_file,
                filename=f"vivienda_galeria_{instance.vivienda.id_vivienda}_{imagen_file.name}",
                content_type=imagen_file.content_type
            )
        if commit:
            instance.save()
        return instance


class ViviendaImagenInline(admin.TabularInline):
    model = ViviendaImagen
    form = ViviendaImagenForm
    extra = 5
    max_num = 5
    readonly_fields = ('miniatura', 'fecha_registro')

    def miniatura(self, obj):
        if obj.imagen_url:
            return format_html('<img src="{}" style="width: 80px; height:auto;" />', obj.imagen_url)
        return "-"
    miniatura.short_description = "Imagen"




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

class CaracteristicaViviendaInline(admin.TabularInline):
    model = CaracteristicaVivienda
    extra = 1
    max_num = 10
    fields = ('tipo', 'nombre', 'descripcion','cantidad', 'fecha_registro')
    readonly_fields = ('fecha_registro',)

@admin.register(Vivienda)
class ViviendaAdmin(admin.ModelAdmin):
    form = ViviendaAdminForm
    list_display = (
        'nombre', 
        'miniatura_portada', 
        'tipo', 
        'departamento', 
        'estado', 
        'precio', 
        'permite_financiamiento',
        'comprador',
        'superficie', 
        'fecha_registro',
        'contador_galeria',
        'contador_caracteristicas'
    )
    list_filter = ('estado', 'tipo', 'departamento', 'permite_financiamiento','comprador')
    search_fields = ('nombre',)
    readonly_fields = ('fecha_registro', 'fecha_actualizacion', 'portada_url', 'miniatura_portada')
    inlines = [ViviendaImagenInline, CaracteristicaViviendaInline]

    fieldsets = (
        ('Información General', {
            'fields': (
                'nombre', 'tipo', 'departamento', 'descripcion', 
                'precio', 'permite_financiamiento',
                'portada_url', 'portada_file', 'estado','comprador','superficie', 'latitude', 'longitude'
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

    def contador_galeria(self, obj):
        return obj.galeria.count()
    contador_galeria.short_description = "Imágenes"

    def contador_caracteristicas(self, obj):
        return obj.caracteristicas.count()
    contador_caracteristicas.short_description = "Características"

