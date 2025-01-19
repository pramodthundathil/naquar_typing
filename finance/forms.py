from django import forms
from .models import Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['particulars', 'amount', "bill_number","payment_mode", 'other']
        labels = {
            'particulars': 'Particulars',
            'amount': 'Amount',
            'other': 'Partner Details',
        }
        widgets = {
            'particulars': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'income-particulars',
                'placeholder': 'Enter particulars'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'income-amount',
                'placeholder': 'Enter amount',
                "min":0
            }),
            'other': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'income-other',
                'placeholder': 'Other details'
            }),
            'bill_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'billno',
                'placeholder': 'Bill Number (Optional)'
            }),
            "payment_mode": forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_mode',
                'placeholder': 'Payment Mode'
            })
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['particulars',"bill_number","payment_mode", 'amount', 'other']
        labels = {
            'particulars': 'Particulars',
            'amount': 'Amount',
            'other': 'Partner Details',
        }
        widgets = {
            'particulars': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'expense-particulars',
                'placeholder': 'Enter particulars'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'expense-amount',
                'placeholder': 'Enter amount',
                "min":0
            }),
            'other': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'expense-other',
                'placeholder': 'Other details',
               
            }),
            'bill_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'billno',
                'placeholder': 'Bill Number (Optional)'
            }),
            "payment_mode": forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_mode',
                'placeholder': 'Payment Mode'
            })
        }
