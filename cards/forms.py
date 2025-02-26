from django import forms
from .models import CardCreate


class CardCreateForm(forms.ModelForm):

    class Meta:
        model = CardCreate
        fields = '__all__'
        widgets = {
            'defesa': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 99, 'step': 1, }),
            'passe': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 99, 'step': 1, }),
            'habilidade': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 99, 'step': 1, }),
            'chute': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 99, 'step': 1, }),
            'duelo': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 99, 'step': 1, }),
            'fisico': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 99, 'step': 1, }),
        }
