import random

SET_OF_VALUES = 'abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ_0123456789'



def generate_key():
    """
    Generates a 12 digit random value as a key

    """
    unique_id = "".join([random.choice(SET_OF_VALUES) for i in range(12)])
    return unique_id