import requests
from docassemble.DATools.nocodb import list_nocodb_record

def get_questions_from_nocodb(table_id: str, filter: str= ""):
    data = list_nocodb_record(table_id=table_id, fields="label,field,datatype,input type,choices,show if,help", filter=filter)

    updated_data = []
    for entry in data:
        updated_entry = {k: v for k, v in entry.items() if v is not None}
        updated_data.append(updated_entry)

    return updated_data

def save_spolek_data(data):
    output = flatten_json(data["Spolek"])

    requests.post('https://hook.eu1.make.com/qajj4d9qshooixotv4ywkhf6isdqvf5j', data=output,headers={'Content-Type': 'application/json'})

    return True


def flatten_json(data):
    result = {}
    for key, value in data.items():
        if key in ("_class", "instanceName"):  # Skip these keys
            continue

        if isinstance(value, dict):
            result.update(flatten_json(value, key))  # Recurse for nested dicts
        else:
            result[key] = value

    return result