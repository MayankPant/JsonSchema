from typing import Any

from django.http import HttpRequest
from .models import User
from rest_framework import status

class UserAuth:
    
    def authenticate(request: HttpRequest, username=None, password=None, **kwargs):
        if request.method == 'POST':
            try:
                user = User.objects.get(username = username)
                print(user)
                if type(user) ==  User and user.password_hash == password:
                    return user
                else:
                    return None
            except User.DoesNotExist:
                return None
        else:
            return None



    def get_user(self, request: HttpRequest, username=None, **kwargs):
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        return user
            
