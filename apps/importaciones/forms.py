from django import forms
from .models import Importacion

class ImportacionForm(forms.ModelForm):
    class Meta:
        model = Importacion
        fields = [
            'nombre',
            'tipo_importacion',
            'servicios_asociados',
            'proveedores',
            'proceso_trabajo',
            'observaciones'
        ]
