from django import forms
from .models import ProcesoInterno, Proceso

class ProcesoInternoForm(forms.ModelForm):
    class Meta:
        model = ProcesoInterno
        fields = ['titulo', 'descripcion', 'responsables']

class ProcesoForm(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = [
            'proceso_interno',
            'usuario',
            'lote',
            'vivienda',
            'titulo',
            'descripcion',
            'estado',
            'requisitos',
            'documentos',
            'observaciones',
        ]
