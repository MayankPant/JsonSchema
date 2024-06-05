from typing import Any

from django.http import HttpRequest
from .models import User
from rest_framework import status
from .utils import validate_password
import logging
logger =  logging.getLogger('editor')


class UserAuth:
    
    def authenticate(request: HttpRequest, username=None, password=None, **kwargs):
        if request.method == 'POST':
            try:
                user = User.objects.get(username = username)
                if type(user) ==  User:
                    """
                    Authentication using brcrypt involves first taking the plain text password from user. It then takes the hashed
                    value from the database, takes the salt used from it, uses this salt in check password to create the hashvalue
                    and then compares this new hash value to the database hashvalue to compare the password
                    """
                    logger.debug(validate_password(password, user.password_hash))
                    if validate_password(password,  user.password_hash): # compare user password with the stored hashed password
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
            
