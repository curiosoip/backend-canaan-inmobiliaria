# apps/viviendas/api/serializers.py
from rest_framework import serializers
from .models import TipoVivienda, Vivienda, ViviendaImagen,CaracteristicaVivienda
from apps.usuarios.serializers import UsuarioSerializer 

class ViviendaImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViviendaImagen
        fields = [
            'id_imagen',
            'imagen_url',
            'fecha_registro',
        ]


class TipoViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVivienda
        fields = [
            'id_tipo',
            'nombre',
            'descripcion',
            'fecha_registro',
            'fecha_actualizacion',
        ]

class CaracteristicaViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicaVivienda
        fields = ['id_caracteristica', 'tipo', 'nombre', 'descripcion','cantidad', 'fecha_registro']  # quitar 'cantidad'

class ViviendaSerializer(serializers.ModelSerializer):
    tipo = TipoViviendaSerializer(read_only=True)
    comprador = UsuarioSerializer(read_only=True)
    galeria = ViviendaImagenSerializer(many=True, read_only=True)
    caracteristicas = CaracteristicaViviendaSerializer(many=True, read_only=True)  

    class Meta:
        model = Vivienda
        fields = [
            'id_vivienda',
            'nombre',
            'descripcion',
            'portada_url',
            'estado',
            'latitude',
            'longitude',
            'precio',
            'permite_financiamiento',
            'tipo',
            'comprador',
            'superficie',
            'galeria',
            'caracteristicas',
            'fecha_actualizacion',
        ]

