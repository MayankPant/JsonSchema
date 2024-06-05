import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import logging
logger = logging.getLogger('editor')


SET_OF_VALUES = 'abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ_0123456789'



def generate_key():
    """
    Generates a 12 digit random value as a key

    """
    unique_id = "".join([random.choice(SET_OF_VALUES) for i in range(12)])
    return unique_id


def password_hasher(password):
    """
    Uses bcrypt encryption to hash passwords
    
    """
    hashed_password = make_password(password)
    return hashed_password

def validate_password(password, hashed_password):
    return check_password(password, hashed_password)

