from django import forms
from .models import Services

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = [
            'title', 
            'description', 
            'authority', 
            'total_fund_from_customer', 
            "govt_fee",
            'tax', 
            'tax_value'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title',"placeholder":"Enter Service Title"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': 3, "placeholder":"Enter Service Description"}),
            'authority': forms.TextInput(attrs={'class': 'form-control', 'id': 'authority', "placeholder":"Enter Authority"}),
            'total_fund_from_customer': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price', "placeholder":"Enter Price"}),
            'govt_fee': forms.NumberInput(attrs={'class': 'form-control', 'id': 'govt_fee', "placeholder":"Enter Govt Fee"}),
            'tax': forms.Select(attrs={'class': 'form-control', 'id': 'tax', "placeholder":"Enter Tax"}),
            'tax_value': forms.Select(attrs={'class': 'form-control', 'id': 'tax_value', "placeholder":"Enter Tax Value"}),
        }


from .models import Customers
class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'email', 'phone', 'address', 'eid_number', 'customer_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address', 'rows': 3}),
            'eid_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter EID number'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
        }