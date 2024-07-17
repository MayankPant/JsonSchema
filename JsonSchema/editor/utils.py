import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import logging
logger = logging.getLogger('editor')
import jsonschema
import json
from django.core.cache import cache
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

session = SessionStore()


SET_OF_VALUES = 'abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ_0123456789'
OTP_LENGTH = 4
EXPIRY_TIME = 10


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

class JsonSchemaValidator():

    def __init__(self) -> None:
        pass
    
    def validate(self, schema, user_input):
        try:
            schema = json.loads(schema)
            user_input = json.loads(user_input)
            jsonschema.validate(schema=schema, instance=user_input)
            print("JSON SCHEMA VALIDATED")
            return True
        except jsonschema.ValidationError as e:
            print("JSON SCHEMA VALIDATION UNSUCCESSFUL")
            return False
        except Exception as e:
            print(f"Exception occured: {e}\n\n\n\n\n")
            return False
        
    def validate_jsonschema(self, schema):
        """
        The most widely used json schema is the draft7 schema and so
        we will be using it here, atleast for now

        """
        print(f"Recieved schema for validation: {schema}\n\n\n\n")
        try:
            schema = json.loads(schema)
            jsonschema.Draft7Validator.check_schema(schema=schema)
            return True
        except jsonschema.ValidationError as e:
            print("Validation Error")
            return False
        except Exception as e:
            print(f"Exception occured: {e}\n\n\n\n\n")
            return False
        
def otp_generator(length: int = OTP_LENGTH, expiry_time: int = EXPIRY_TIME, user_email: str = None):
    try:
        otp = "".join([random.choice("0123456789") for _ in range(length)])
        print(f"OTP Details: {otp}")
        cache.set(user_email, otp, expiry_time * 60)  # converting minutes to seconds
        response = django_send_mail(
            subject="Password Change OTP",
            message=f"Your OTP is {otp}",
            from_email=None, #use the default value
            recipient_list=[user_email]
        )
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print("Failed to send email. ", response.content)
    except Exception as e:
        print(f"Error: {e}")

def django_send_mail(subject: str, message: str, from_email: str,  recipient_list: list):
    try:
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
        return HttpResponse("Email sent successfully!", status=200)
    except Exception as e:
        return HttpResponse(f"Error sending email: {str(e)}", status=500)