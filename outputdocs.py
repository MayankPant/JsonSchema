def output_docs(schema):
    with open("output.md", 'w') as openfile:
        openfile.write("# Selected schema documentation\n\n\n")
        openfile.write("## Overview\n\n")

        if(schema.get("title") != None):
            openfile.write("*title* : " + schema.get("title"))
        else:
            openfile.write("*title* : Has the title of the schema\n")

        if(schema.get("description") != None):
            openfile.write("*Description* : " + schema.get("description"))
        else:
            openfile.write("*Description* : Has the Description of the schema\n")

        queueSchema = []
        currSchema = schema.get("properties")
        queueSchema.append(currSchema)

        while len(queueSchema) != 0:
            ""
            

        



output_docs({})
























































































































































































































































































































