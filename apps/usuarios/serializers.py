# apps/usuarios/api/serializers.py
from rest_framework import serializers
from .models import Usuario, Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = [
            'id_rol',
            'nombre',
            'descripcion',
            'fecha_registro',
            'fecha_actualizacion',
        ]


class UsuarioSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)  # devuelve el rol anidado

    class Meta:
        model = Usuario
        fields = [
            'id_usuario',
            'username',
            'first_name',
            'last_name',
            'email',
            'rol',
            'celular',
            'foto_url',
            'is_active',
            'fecha_registro',
            'fecha_actualizacion',
        ]
