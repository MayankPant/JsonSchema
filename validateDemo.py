
import json
def validate(schema, data):
    queueSchema = []
    queueSchema.append(schema)
    queueData = []
    queueData.append(data)
    map  = {"string" : str, "integer" : int, "object" : dict, "number" : int}

    while len(queueSchema) != 0:
        currSchema = queueSchema.pop()
        currData = queueData.pop()
        requirements = currSchema.get("required")
        print(requirements)
        for req in requirements:
            print(type(currData.get(req)))
            print(map.get(currSchema.get("properties").get(req).get("type")))
            if not (req in currData):
                return False
            
            # elif not type(currData.get(req)) is map.get(currSchema.get("properties").get(req).get("type")):
            #       return False
            
            if currSchema.get("properties").get(req).get("type") == "object":
                queueSchema.append(currSchema.get("properties").get(req))
                queueData.append(currData.get(req))
            
    return True



user_file = {
    "productID" : 123,
    "price" : 31,
    "dimensions" : {
        "length" : {
            "thickness" : 2,
            "youngs modulus" : 0.9
        },
        "breadth" : 20,
        "height" : 30
    }
}

openFile = open("data/jsonFile.json", 'r')

schema = json.loads(openFile.read())

if(validate(schema, user_file)):
    print("json is valid")
else:
    print("json not valid")




