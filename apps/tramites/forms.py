from django import forms
from .models import Tramite, Requisito


class TramiteForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = [
            'departamentos',
            'nombre',
            'descripcion',
            'costo',
            'tiempo_estimado',
            'activo',
        ]


class RequisitoForm(forms.ModelForm):
    class Meta:
        model = Requisito
        fields = [
            'tramite',
            'nombre',
            'descripcion',
            'obligatorio',
            'archivo_requerido',
            'orden',
        ]
