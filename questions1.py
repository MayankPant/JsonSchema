# Sample nested dictionary with more details
nested_dict = {
    'person1': {
        'name': 'John',
        'age': 30,
        'contact_info': {
            'email': 'john@example.com',
            'phone': '555-1234'
        },
        'address': {
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001'
        }
    },
    'person2': {
        'name': 'Jane',
        'age': 25,
        'contact_info': {
            'email': 'jane@example.com',
            'phone': '555-5678'
        },
        'address': {
            'city': [{
                "address": "str"
            },],
            'state': 'CA',
            'zip_code': '94105'
        }
    },

    'person3' : {
    'name': 'Mike',
    'age': 28,
    'contact_info': {
        'email': 'mike@example.com',
        'phone': '555-9876'
    },
    'address': {
        'city': 'Los Angeles',
        'state': 'CA',
        'zip_code': '90001'
    }


    }
}


# Updating values
nested_dict['person1']['age'] = 31
nested_dict['person2']['address']['zip_code'] = '94110'



        
def findKeyInDict(target, data, result):

    if isinstance(data, list) or isinstance(data, tuple):
        for item in data:
            findKeyInDict(target, item, result)
    else:
        for key in data.keys():
            if key == target:
                result.append(data[key])
            
            if type(data[key]) in [dict, list, tuple]:
                findKeyInDict(target, data[key], result)
        


result = []
target = "address"

findKeyInDict(target, nested_dict, result)
print(result)

if len(result) != 0:
    print(result)
else:
    print("no value found")

            
