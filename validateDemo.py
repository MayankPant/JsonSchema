import jsonschema
import json
def validate(schema, data):
    ""



user_file = input()

openFile = open("data/json_File.json", 'r')

schema = json.loads(openFile.read())

validate(schema, user_file)




