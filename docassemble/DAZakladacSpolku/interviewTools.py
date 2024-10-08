import requests
import json

from docassemble.base.util import validation_error

from docassemble.DATools import nocodb

def get_questions_from_nocodb(table_id: str, filter: str= ""):
    data = nocodb.list_nocodb_record(table_id=table_id, fields="label,field,datatype,input type,choices,show if,help,hint,validate,note,css class", filter=filter)

    updated_data = []
    for entry in data:
        updated_entry = {k: v for k, v in entry.items() if v is not None}
        updated_data.append(updated_entry)

    return updated_data

def save_spolek_data(data: dict, row_id: int):

    data = {
        "dataSpolek": json.dumps(data["Spolek"])
    }

    results = nocodb.update_record(table_id="mkejxthrd05vdcc", content=data, row_id=row_id)

    return results

def step_done(step: int, row_id: int):

    progress = nocodb.get_record(table_id="mkejxthrd05vdcc", row_id=row_id, fields="progress")

    progress["progress"][step] = True
    
    results = nocodb.update_record(table_id="mkejxthrd05vdcc", content=progress, row_id=row_id)
    
    return progress, results

def call_with_error_check(url):
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as error:
        return error  # Return the exception object itself

def get_document_url(row_id: int, document: str):

    match document:
        case "stanovy":
            # TODO: Upravit URL na univerzální variantu pro testovací i ostrou verzi.
            return call_with_error_check(f"https://da-test.frankbold.org/interview?i=docassemble.playground1ZakladacSpolku:gen_stanovy.yml&reset=1&spolek_id={row_id}")
        

def load_spolek_data(id: int):

    data = nocodb.list_nocodb_record(table_id="mkejxthrd05vdcc", fields="dataSpolek", filter=f"(Id,eq,{id})")

    if len(data) == 1:
        return flatten_json(data[0]["dataSpolek"])
    else:
        return False

def flatten_json(data, prefix=''):
    result = {} 
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ("_class", "instanceName", "ask_number","ask_object_type","auto_gather","complete_attribute","minimum_number","object_type","object_type_parameters", "there_are_any"):  # Skip these keys
                continue
            elif key == "important":
                result[f"{prefix}.{key}" if prefix else key] = value
                continue

            new_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict) or isinstance(value, list):
                result.update(flatten_json(value, new_key))  # Recurse for nested dicts or lists
            else:
                result[new_key.replace(".elements","")] = value

    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_key = f"{prefix}[{index}]"

            if isinstance(value, dict) or isinstance(value, list):
                result.update(flatten_json(value, new_key))  # Recurse for nested dicts or lists
            else:
                result[new_key.replace(".elements","")] = value

    return result

def contains_spolek(x):
  x = x.lower()
  if "spolek" in x:
    return True
  elif "z. s." in x:
    return True
  elif "zapsaný spolek" in x:
    return True
  else:
    validation_error('Název spolku <strong>musí</strong> obsahovat "z. s.", "spolek", nebo "zapsaný spolek"')
  return

def string_2_pole(x):
  x = x.split('\r\n')
  return x
