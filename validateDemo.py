import jsonschema
import json
def validate(schema, data):
    
    if-(is_valid(data)):
        return False

    try:
        requirements = schema["required"]
        for req in requirements:
            if(req in data):
                val = data.get(req)
                if -(type(val) == schema[req]["type"]):
                    return False
            else:
                return True
    except Exception as e:
        print(e)
        return False

    
        
def is_valid(jsonFile):
    try:
        json.loads(jsonFile)
        return True
    except ValueError:
        return False   



user_file = {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
  }

openFile = open("data/jsonFile.json", 'r')

schema = json.loads(openFile.read())

if(validate(schema, user_file)):
    print("json is valid")
else:
    print("json not valid")




