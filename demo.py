import json
import jsonschema

schema = {
    "title" : "product",
    "type" : "object",
    "description" :  "A product in the catalog",
    "properties" : {
        "productID" : {
            "type" : "integer"
        },
        "productName" : {
            "type" : "string"
        },
        "price" : {
            "type" : "number",
            "exclusiveMinimum" : 30
        },
        "tags" : {
            "type" : "array",
            "desctiption" : "The tage for the product",
            "items" : {
                "type" : "string"
            },
            "minItems" : 1,
            "uniqueItems" : True
        },
        "dimensions" : {
            "type" : "object",
            "properties" : {

                "length" : {

                    "type" : "object",
                    
                    "properties" : {
                        "thickness" : {
                            "type" : "integer"
                        },
                        "youngs modulus" : {
                            "type" : "number"
                        }
                    },


                    "required" : ["thickness", "youngs modulus"]
                
                },
                "breadth"  : {
                    "type" : "number"
                },
                "height" : {
                    "type" : "number"
                }
            },

            "required" : ["length", "breadth", "height"]
        }


    },

    "required" : ["productID", "price", "dimensions"]
}


user_data = {
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
            
            elif not type(currData.get(req)) is map.get(currSchema.get("properties").get(req).get("type")):
                  return False
            
            if currSchema.get("properties").get(req).get("type") == "object":
                queueSchema.append(currSchema.get("properties").get(req))
                queueData.append(currData.get(req))
            
    return True
            
        
# type(9) is int
# type(2.5) is float
# type('x') is str
# type(u'x') is unicode
# type(2+3j) is complex

# There are a few other cases.

# isinstance( 'x', basestring )
# isinstance( u'u', basestring )
# isinstance( 9, int )
# isinstance( 2.5, float )
# isinstance( (2+3j), complex )



if(validate(schema, user_data)):
    print("json is valid")
else:
    print("json is not valid")

