import random

SET_OF_VALUES = 'abcdefghijklmnopqurstuvwxyz_0123456789'

def generate_key():
    unique_id = "".join([random.choice(SET_OF_VALUES) for i in range(12)])
    return unique_id