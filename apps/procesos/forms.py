from django import forms
from .models import ProcesoInterno, Proceso,PasoProcesoInterno

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

class PasoProcesoInternoForm(forms.ModelForm):
    class Meta:
        model = PasoProcesoInterno
        fields = ['orden', 'titulo']
        widgets = {
            'orden': forms.NumberInput(attrs={
                'class': 'border rounded p-2 w-full',
                'placeholder': 'Número de orden'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'border rounded p-2 w-full',
                'placeholder': 'Título del paso'
            }),
        }