import requests
import json

from docassemble.base.util import validation_error

from docassemble.DATools.nocodb import list_nocodb_record, update_record

def get_questions_from_nocodb(table_id: str, filter: str= ""):
    data = list_nocodb_record(table_id=table_id, fields="label,field,datatype,input type,choices,show if,help,hint,validate,note", filter=filter)

    updated_data = []
    for entry in data:
        updated_entry = {k: v for k, v in entry.items() if v is not None}
        updated_data.append(updated_entry)

    return updated_data

def save_spolek_data(data: dict):

    row_id = data["Spolek"]["row_id"]

    data = {
        "dataSpolek": json.dumps(data["Spolek"])
        #"dataSpolek": json.dumps(flatten_json(data["Spolek"]))
    }
    #temp
    results = update_record(table_id="mkejxthrd05vdcc", content=data, row_id=row_id)

    return results

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

    data = list_nocodb_record(table_id="mkejxthrd05vdcc", fields="dataSpolek", filter=f"(Id,eq,{id})")

    if len(data) == 1:
        return flatten_json(data[0]["dataSpolek"])
    else:
        return False

def flatten_json(data, prefix=''):
    result = {}
    for key, value in data.items():
        if key in ("_class", "instanceName"):  # Skip these keys
            continue

        new_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            result.update(flatten_json(value, new_key))  # Recurse for nested dicts
        else:
            result[new_key] = value

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