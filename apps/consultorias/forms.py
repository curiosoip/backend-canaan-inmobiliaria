from django import forms
from .models import Consultoria

class ConsultoriaForm(forms.ModelForm):
    class Meta:
        model = Consultoria
        fields = [
            'nombre',
            'descripcion_general',
            'servicios_especializados',
            'proceso_trabajo',
        ]
