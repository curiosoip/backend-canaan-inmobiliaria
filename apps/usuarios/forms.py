# apps/usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Rol
from django.contrib.auth.hashers import make_password


class UsuarioRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=False)
    celular = forms.CharField(max_length=25, required=False)
    foto_url = forms.URLField(required=False)

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "rol",
            "celular",
            "foto_url",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email


class UsuarioUpdateForm(forms.ModelForm):
    foto_file = forms.FileField(required=False, label="Foto de perfil")
    
    class Meta:
        model = Usuario
        fields = ["username", "email", "rol", "celular", "foto_file", "first_name", "last_name"]

    def save(self, commit=True):
        usuario = super().save(commit=False)

        foto_file = self.cleaned_data.get("foto_file")
        if foto_file:
            from utils.storages.r2_storage import upload_to_r2
            usuario.foto_url = upload_to_r2(
                foto_file,
                filename=f"usuario_foto_{usuario.id_usuario}_{foto_file.name}",
                content_type=foto_file.content_type
            )

        if commit:
            usuario.save()
        return usuario



class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del Rol'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción (opcional)',
                'rows': 3
            }),
        }
        labels = {
            'nombre': 'Nombre del Rol',
            'descripcion': 'Descripción',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Rol.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un rol con este nombre.")
        return nombre


class RolUpdateForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UsuarioModalForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    foto_file = forms.FileField(required=False, label="Foto de perfil")
    first_name = forms.CharField(required=True, label="Nombres")
    last_name = forms.CharField(required=True, label="Apellidos")

    class Meta:
        model = Usuario
        fields = ["username", "email", "rol", "celular", "foto_file", "password", "first_name", "last_name"]

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.password = make_password(self.cleaned_data["password"])  
        usuario.first_name = self.cleaned_data["first_name"]
        usuario.last_name = self.cleaned_data["last_name"]

        if commit:
            usuario.save()

        foto_file = self.cleaned_data.get("foto_file")
        if foto_file:
            from utils.storages.r2_storage import upload_to_r2
            usuario.foto_url = upload_to_r2(
                foto_file,
                filename=f"usuario_foto_{usuario.id_usuario}_{foto_file.name}",
                content_type=foto_file.content_type
            )
            usuario.save()  # Guardar de nuevo con la URL de la foto

        return usuario
