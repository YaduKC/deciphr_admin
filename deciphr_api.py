from urllib import response
import requests

from app import header

base_url = "https://api.deciphr.ai"
staging_url = "http://13.210.61.239:9999"

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
    url = f"{staging_url}/key_quotes/{file_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def search_listennotes(query, sort_by, type_, min_length, max_len, genre, published_before, publised_after, only_in, token, offset: int=0):
    url = f"{staging_url}/listennotes/search/?query={query}?sort_by={sort_by}?type={type_}?offset={offset}?min_len=10?max_len=240?genre_ids={genre}?published_before={published_before}?published_after={publised_after}?only_in={only_in}?language=English"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def send_email_verification(email, token):
    url = f"{base_url}/signup/resend-verification-email"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "email": email,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def prospective_user_process(file_name, start_timestamp, end_timestamp, audio_url, token):
    url = f"{staging_url}/prospective/process"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "audio_url":audio_url,
        "start_timestamp":start_timestamp,
        "end_timestamp":end_timestamp,
        "title":file_name
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_prospective_process_status(file_id, token):
    url = f"{staging_url}/up/details/{file_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()
