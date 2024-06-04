from .models import User
from django import forms

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password_hash']
