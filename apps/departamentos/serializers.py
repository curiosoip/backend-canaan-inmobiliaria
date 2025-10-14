# apps/departamentos/api/serializers.py
from rest_framework import serializers
from apps.departamentos.models import Departamento
from apps.urbanizaciones.serializers import UrbanizacionSerializer
from apps.viviendas.serializers import ViviendaSerializer
from apps.tramites.serializers import TramiteSerializer

class DepartamentoSerializer(serializers.ModelSerializer):
    urbanizaciones = UrbanizacionSerializer(many=True, read_only=True)
    viviendas = ViviendaSerializer(many=True, read_only=True)
    tramites = TramiteSerializer(many=True, read_only=True)
    total_viviendas = serializers.IntegerField(read_only=True)
    total_urbanizaciones = serializers.IntegerField(read_only=True)
    total_tramites = serializers.IntegerField(read_only=True)

    class Meta:
        model = Departamento
        fields = [
            'id_departamento', 'nombre', 'latitude', 'longitude',
            'total_urbanizaciones', 'total_viviendas', 'total_tramites',
            'urbanizaciones', 'viviendas', 'tramites'
        ]
