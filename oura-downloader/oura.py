import os
import json
import requests

OURA_API_URL = 'https://api.oura.io/api/v2/'


def fetch_by_webhook(payload, auth_data):
    
    data_type = payload["data_type"]
    user_id = payload["user_id"]
    object_id = payload["object_id"]

    # Map between oura IDs and study-ids, also fetch relevant access tokens
    # (Missing values will cause a key error which should crash back to calling function)
    participant_id = auth_data['patient_map'][user_id]
    token = auth_data['tokens'][participant_id]["access_token"]

    # Retrieve the data for this document from the Oura API
    url = f"{OURA_API_URL}/{data_type}/{object_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Queried {url} for {participant_id}/{data_type}: {response.status_code}")
    response.raise_for_status()
    oura_data = response.json()

    return data_type, oura_data
