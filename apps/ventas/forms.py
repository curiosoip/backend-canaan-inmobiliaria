from django import forms
from .models import Venta
from decimal import Decimal

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = [
            'usuario',
            'lote',
            'vivienda',
            'tipo_venta',
            'monto_total',
            'monto_inicial',
            'saldo_restante',
            'total_cuotas',
            'tasa_interes',
            'banco_monto',
            'empresa_monto',
            'estado',
        ]
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'lote': forms.Select(attrs={'class': 'form-control'}),
            'vivienda': forms.Select(attrs={'class': 'form-control'}),
            'tipo_venta': forms.Select(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monto_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'saldo_restante': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_cuotas': forms.NumberInput(attrs={'class': 'form-control'}),
            'tasa_interes': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'banco_monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'empresa_monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if monto_total <= 0:
            raise forms.ValidationError("El monto total debe ser mayor que cero.")
        return monto_total

    def clean_monto_inicial(self):
        monto_inicial = self.cleaned_data.get('monto_inicial') or Decimal('0.00')
        monto_total = self.cleaned_data.get('monto_total') or Decimal('0.00')
        if monto_inicial > monto_total:
            raise forms.ValidationError("El monto inicial no puede ser mayor que el monto total.")
        return monto_inicial

    def clean_saldo_restante(self):
        saldo = self.cleaned_data.get('saldo_restante')
        monto_total = self.cleaned_data.get('monto_total') or Decimal('0.00')
        monto_inicial = self.cleaned_data.get('monto_inicial') or Decimal('0.00')
        if saldo is None:
            saldo = monto_total - monto_inicial
        elif saldo < 0:
            raise forms.ValidationError("El saldo restante no puede ser negativo.")
        return saldo
