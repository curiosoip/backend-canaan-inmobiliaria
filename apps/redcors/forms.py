# apps/redcors/forms.py
from django import forms
from .models import RedCORS

class RedCORSForm(forms.ModelForm):
    class Meta:
        model = RedCORS
        fields = [
            'nombre_proyecto',
            'tipo_servicio',
            'descripcion',
            'proveedor',
            'observaciones',
        ]
