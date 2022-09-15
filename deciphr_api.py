from urllib import response
import requests

from app import header

base_url = "https://api.deciphr.ai"

def login(email: str, password: str):
    url = f"{base_url}/login"
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(url, json=data)
    return response.json()

def get_user_transcripts(token):
    url = f"{base_url}/up/all"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_user_audio(token):
    url = f"{base_url}/up/all-audio"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_file_data(token, file_id):
    url = f"{base_url}/up/details/{file_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_quotes(token, file_id):
    url = f"http://13.210.61.239:9999/key_quotes/{file_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()
    