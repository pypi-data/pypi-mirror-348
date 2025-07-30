import requests
import io
import json
import time

def try_upload_text(text_name: str, text: str, token: str, metadata: dict = {}, chunk_size: int = 1000, overwrite: bool = True):
    if not token:
        raise ValueError("Invalid token field")

    overwrite_param = 'true' if overwrite else 'false'
    url = f'https://api.voiceflow.com/v1/knowledge-base/docs/upload?overwrite={overwrite_param}&maxChunkSize={chunk_size}'
    headers = {
            "accept": "application/json",
            "Authorization": token
        }
    
    if metadata:
        metadata = {
            'metadata': json.dumps(metadata)
        }

    with io.BytesIO(text.encode('utf-8-sig')) as txt_file:
        files = {
            "file": (f'{text_name}.txt', txt_file, "text/plain")
        }
        response = requests.post(url, headers=headers, files=files, data=metadata)
        response.raise_for_status()
        return response.json()


def try_upload_table(table_name: str, items: list, token: str, searchable_fields: list, metadata_fields: list=[], overwrite=True):
    if not token:
        raise ValueError("Invalid token field")
    
    json_data = {
        "data": {
            "name": table_name,
            "schema": {
                "searchableFields": searchable_fields,
                "metadataFields": metadata_fields,
            },
            "items": items
        }
    }
        
    url = "https://api.voiceflow.com/v1/knowledge-base/docs/upload/table"
    if overwrite:
        url += "?overwrite=true"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": token
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


def was_document_uploaded(document_id, token):
    url = f"https://api.voiceflow.com/v1/knowledge-base/docs/{document_id}"
    headers = {
        "accept": "application/json",
        "Authorization": token
        }
    
    time.sleep(10)
    for i in range(5):
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        status = response.json()["data"]["status"]["type"]
        if status.lower() == "success":
            return True
        
        time.sleep(20)

    return False