import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import logging
logger = logging.getLogger('editor')
import jsonschema
import json


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


