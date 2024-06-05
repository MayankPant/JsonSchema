from .models import User
from django import forms

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password_hash', 'profile_picture', 'user_email', 'created_at']
