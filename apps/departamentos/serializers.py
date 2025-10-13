# apps/departamentos/api/serializers.py
from rest_framework import serializers
from apps.departamentos.models import Departamento

class DepartamentoSerializer(serializers.ModelSerializer):
    total_viviendas = serializers.IntegerField()
    total_urbanizaciones = serializers.IntegerField()
    total_tramites = serializers.IntegerField()

    class Meta:
        model = Departamento
        fields = [
            'id_departamento', 'nombre', 'latitude', 'longitude',
            'total_viviendas', 'total_urbanizaciones', 'total_tramites'
        ]
