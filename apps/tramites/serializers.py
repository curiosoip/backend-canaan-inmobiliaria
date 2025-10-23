# apps/tramites/api/serializers.py
from rest_framework import serializers
from .models import Tramite, Requisito

class RequisitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisito
        fields = [
            'id_requisito_tramite',
            'nombre',
            'descripcion',
            'obligatorio',
            'archivo_requerido',
            'orden',
            'fecha_registro',
            'fecha_actualizacion',
        ]


class TramiteSerializer(serializers.ModelSerializer):
    requisitos = RequisitoSerializer(many=True, read_only=True)  # incluye requisitos relacionados

    class Meta:
        model = Tramite
        fields = [
            'id_tramite',
            'nombre',
            'descripcion',
            'costo',
            'tiempo_estimado',
            'activo',
            'fecha_registro',
            'fecha_actualizacion',
            'requisitos',
        ]
