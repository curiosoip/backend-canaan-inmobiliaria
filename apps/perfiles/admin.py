from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Perfil, DocumentoUsuario
from utils.storages.r2_storage import upload_to_r2  # tu función de subida a R2
from apps.ventas.models import Venta
from apps.pagos.models import Pago
from apps.cuotas.models import Cuota


class DocumentoUsuarioForm(forms.ModelForm):
    archivo_file = forms.FileField(required=False, label="Archivo del documento")

    class Meta:
        model = DocumentoUsuario
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        archivo_file = self.cleaned_data.get("archivo_file")
        if archivo_file:
            instance.archivo_url = upload_to_r2(
                archivo_file,
                filename=f"documento_{instance.id}_{archivo_file.name}",
                content_type=archivo_file.content_type
            )

        if commit:
            instance.save()
        return instance


@admin.register(DocumentoUsuario)
class DocumentoUsuarioAdmin(admin.ModelAdmin):
    form = DocumentoUsuarioForm
    list_display = ('perfil', 'requisito', 'archivo_enlace', 'fecha_subida')
    search_fields = ('perfil__usuario__username', 'requisito__nombre')
    readonly_fields = ('fecha_subida', 'archivo_enlace')

    def archivo_enlace(self, obj):
        if obj.archivo_url:
            return format_html('<a href="{}" target="_blank">Ver archivo</a>', obj.archivo_url)
        return "-"
    archivo_enlace.short_description = "Archivo"


class PerfilForm(forms.ModelForm):
    foto_file = forms.FileField(required=False, label="Foto de perfil")

    class Meta:
        model = Perfil
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        foto_file = self.cleaned_data.get("foto_file")
        if foto_file:
            instance.foto_perfil_url = upload_to_r2(
                foto_file,
                filename=f"perfil_foto_{instance.id}_{foto_file.name}",
                content_type=foto_file.content_type
            )

        if commit:
            instance.save()
        return instance


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    form = PerfilForm
    list_display = ('usuario', 'miniatura_foto', 'direccion', 'fecha_nacimiento', 'fecha_registro')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'direccion')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion', 'miniatura_foto')

    def miniatura_foto(self, obj):
        if obj.foto_perfil_url:
            return format_html('<img src="{}" style="width:50px; height:auto; border-radius:50%;" />', obj.foto_perfil_url)
        return "-"
    miniatura_foto.short_description = "Foto de perfil"

    # Mostrar las relaciones directamente como enlaces
    def ventas_usuario(self, obj):
        ventas = Venta.objects.filter(usuario=obj.usuario)
        return format_html("<br>".join([f"{v}" for v in ventas]))
    ventas_usuario.short_description = "Ventas"

    def pagos_usuario(self, obj):
        pagos = Pago.objects.filter(usuario=obj.usuario)
        return format_html("<br>".join([f"{p}" for p in pagos]))
    pagos_usuario.short_description = "Pagos"

    def cuotas_usuario(self, obj):
        cuotas = Cuota.objects.filter(venta__usuario=obj.usuario)
        return format_html("<br>".join([f"{c}" for c in cuotas]))
    cuotas_usuario.short_description = "Cuotas"
