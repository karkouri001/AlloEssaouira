from django import forms
from .models import CommandeItem

class CommandeItemForm(forms.ModelForm):
    class Meta:
        model = CommandeItem
        fields = ['quantite']
        widgets = {
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }
        labels = {
            'quantite': 'Quantité',
        }
