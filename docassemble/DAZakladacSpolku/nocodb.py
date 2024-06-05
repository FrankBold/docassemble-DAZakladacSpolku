import requests
from docassemble.base.util import get_config

def list_nocodb_record(table_id: str, fields: str = "", viewId: str = "", filter: str= ""):

    url = f"{get_config('nocodbUrl')}/api/v2/tables/{table_id}/records"
    
    headers = {
        "xc-token": get_config('nocodbToken'),
    }

    params = {
        "offset": 0,
        "fields": fields,
        "viewId": viewId,
        "where": filter
    }

    all_records = []

    while True:
        response = requests.get(f"{get_config('nocodbUrl')}/api/v2/tables/{table_id}/records", headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch records: {response.text}")
            break

        data = response.json()
        all_records.extend(data.get('list', []))
        
        # Pagination handling
        page_info = data.get('pageInfo', {})
        print(page_info)
        if page_info.get('isLastPage'):
            break
        else:
            params['offset'] += 25
    
    return all_records