import requests
import json

from docassemble.DATools.nocodb import list_nocodb_record, update_record

def get_questions_from_nocodb(table_id: str, filter: str= ""):
    data = list_nocodb_record(table_id=table_id, fields="label,field,datatype,input type,choices,show if,help", filter=filter)

    updated_data = []
    for entry in data:
        updated_entry = {k: v for k, v in entry.items() if v is not None}
        updated_data.append(updated_entry)

    return updated_data

def save_spolek_data(data: dict):

    row_id = data["Spolek"]["row_id"]

    data = {
        "dataSpolek": json.dumps(flatten_json(data["Spolek"]))
    }

    results = update_record(table_id="mkejxthrd05vdcc", data=data, row_id=row_id)

    return results

def save_document(row_id: int, file_type: str, url_for: str, size: int, mimetype: str = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):

    data = {
        "Stanovy": [{
            "mimetype": mimetype,
            "size": size,
            "title": file_type,
            "url": url_for
        }]
    }

    results = update_record(table_id="mkejxthrd05vdcc", data=data, row_id=row_id)

    return results, data

def load_spolek_data(id: int):

    data = list_nocodb_record(table_id="mkejxthrd05vdcc", fields="dataSpolek", filter=f"(Id,eq,{id})")

    if len(data) == 1:
        return data[0]["dataSpolek"]
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