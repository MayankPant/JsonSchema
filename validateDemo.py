import click
import json


def validate(schema, data):
    queueSchema = []
    queueSchema.append(schema)
    queueData = []
    queueData.append(data)
    map  = {"string" : str, "integer" : int, "object" : dict, "number" : float}

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
            elif currData.get(req) < currSchema.get("properties").get("req").get("exclusiveMinimum"):
                return False
            elif currData.get(req) > currSchema.get("properties").get("req").get("exclusiveMaximum"):
                return False
            
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

@click.command()
@click.option('--schema-file', type=click.Path(exists=True), help='Path to the JSON schema file')
def validate_json(schema_file):
    with open(schema_file, 'r') as file:
        schema = json.load(file)

    # Get JSON data from user input
    data = click.prompt('Enter JSON data: ', type=str)

    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError as e:
        click.echo(f"Error decoding JSON data: {e}")
        return

    if validate(schema, data_dict):
        click.echo("Validation successful!")
    else:
        click.echo("Validation failed!")

validate_json()





