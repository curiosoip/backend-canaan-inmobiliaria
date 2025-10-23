from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.html import format_html
from .models import Rol, Usuario
from utils.storages.r2_storage import upload_to_r2  # si quieres subir fotos desde el admin

class UsuarioAdminForm(forms.ModelForm):
    foto_file = forms.FileField(required=False, label="Foto de perfil")

    class Meta:
        model = Usuario
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        foto_file = self.cleaned_data.get("foto_file")
        if foto_file:
            instance.foto_url = upload_to_r2(
                foto_file,
                filename=f"usuario_foto_{instance.id}_{foto_file.name}",
                content_type=foto_file.content_type
            )

        if commit:
            instance.save()
        return instance

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_registro', 'fecha_actualizacion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    form = UsuarioAdminForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {
            'fields': (
                'first_name', 'last_name', 'email', 'celular', 'rol',
                'foto_url', 'foto_file', 'miniatura_foto'
            )
        }),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('fecha_registro', 'fecha_actualizacion'), 'classes': ('collapse',)}), 
    )
    readonly_fields = ('fecha_registro', 'fecha_actualizacion', 'miniatura_foto')

    list_display = ('username','miniatura_foto', 'email', 'rol', 'is_active', 'fecha_registro')
    search_fields = ('username', 'email')

    def miniatura_foto(self, obj):
        if obj.foto_url:
            return format_html('<img src="{}" style="width:50px; height:auto; border-radius:50%;" />', obj.foto_url)
        return "-"
    miniatura_foto.short_description = "Foto"

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj and obj.rol and obj.rol.nombre.lower() == 'cliente':
            fields = fields + ('password',)
        return fields
