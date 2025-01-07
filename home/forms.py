from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes and IDs to fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f'id_{field_name}',
                'placeholder': f'{field.label}',
            })


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'id_password',
            'placeholder': 'Enter new password (leave blank to keep current password)',
        }),
        help_text="Leave blank if you don't want to change the password."
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes and IDs to other fields
        for field_name, field in self.fields.items():
            if field_name != 'password':  # Skip the custom password field
                field.widget.attrs.update({
                    'class': 'form-control',
                    'id': f'id_{field_name}',
                    'placeholder': f'{field.label}'
                })

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('password')
        if new_password:  # Only set the password if it's not blank
            user.set_password(new_password)
        if commit:
            user.save()
        return user
