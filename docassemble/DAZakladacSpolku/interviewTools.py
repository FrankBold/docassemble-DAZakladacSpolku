from docassemble.DATools.nocodb import list_nocodb_record

def get_questions_from_nocodb(table_id: str, filter: str= ""):
    data = list_nocodb_record(table_id=table_id, fields="label,field,datatype,input type,choices,help", filter=filter)

    updated_data = []
    for entry in data:
        updated_entry = {k: v for k, v in entry.items() if v is not None}
        updated_data.append(updated_entry)

    return updated_data