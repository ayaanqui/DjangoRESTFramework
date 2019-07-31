import json

def isJson(data):
    try:
        jsonData = json.loads(data)
        isValid = True
    except ValueError:
        isValid = False
    return isValid