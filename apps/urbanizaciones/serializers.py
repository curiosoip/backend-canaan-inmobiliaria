# apps/urbanizaciones/api/serializers.py
from rest_framework import serializers
from .models import Urbanizacion, VerticeUrbanizacion, Lote
from apps.usuarios.serializers import UsuarioSerializer

class VerticeUrbanizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerticeUrbanizacion
        fields = [
            'id_vertices_urbanizacion',
            'este_x',
            'norte_y',
            'orden',
            'fecha_registro',
            'fecha_actualizacion',
        ]


class LoteSerializer(serializers.ModelSerializer):
    comprador = UsuarioSerializer(read_only=True)

    class Meta:
        model = Lote
        fields = [
            'id_lote',
            'nombre',
            'area_m2',
            'precio',
            'estado',
            'manzana',
            'fecha_registro',
            'fecha_actualizacion',
            'comprador',
        ]
    
    def get_comprador(self, obj):
        if obj.comprador:
            return {
                "id": str(obj.comprador.id),
                "nombre": obj.comprador.get_full_name() if hasattr(obj.comprador, "get_full_name") else str(obj.comprador)
            }
        return None


class UrbanizacionSerializer(serializers.ModelSerializer):
    vertices = VerticeUrbanizacionSerializer(many=True, read_only=True)
    lotes = LoteSerializer(many=True, read_only=True)

    class Meta:
        model = Urbanizacion
        fields = [
            'id_urbanizacion',
            'nombre',
            'descripcion',
            'portada_url',
            'direccion',
            'latitude',
            'longitude',
            'planimetria_pdf',
            'total_lotes',
            'total_manzanas',
            'area_total',
            'fecha_registro',
            'fecha_actualizacion',
            'vertices',
            'lotes',
        ]
