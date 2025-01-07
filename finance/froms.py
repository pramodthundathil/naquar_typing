from django import forms
from .models import Tax

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['tax_name', 'tax_percentage']
        widgets = {
            'tax_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Tax Name'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Tax Percentage'}),
        }
        labels = {
            'tax_name': 'Tax Name',
            'tax_percentage': 'Tax Percentage (%)',
        }
