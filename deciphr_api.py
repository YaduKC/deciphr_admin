from datetime import timedelta
from urllib import response
import requests
import streamlit as st
from app import header

base_url = "https://api.deciphr.ai"
staging_url = "http://3.219.123.15:9999"

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
    url = f"{base_url}/key_quotes/{file_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def search_listennotes(query, sort_by, type_, min_length, max_len, genre, published_before, publised_after, only_in, token, offset: int=0):
    url = f"{base_url}/listennotes/search/?query={query}?sort_by={sort_by}?type={type_}?offset={offset}?min_len=10?max_len=240?genre_ids={genre}?published_before={published_before}?published_after={publised_after}?only_in={only_in}?language=English"
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
    url = f"{base_url}/prospective/process"
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
    url = f"{base_url}/up/details/{file_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_user_records(token):
    url = f"{base_url}/admin/get_user_records"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def download_file(file_id, format, token):
    url = f"{base_url}/up/download/{file_id}/{format}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.content

def submit_review(key, token):
    url = "http://3.219.123.15:9000/admin/submit_review"
    data = {
        "key": key
    }
    response = requests.post(url, json=data)
    return response.json()

def get_review_results():
    url = "http://3.219.123.15:9000/admin/get_review"
    response = requests.get(url)
    return response.json()

def save_replicate_image(image_url, token, prompt):
    url = "http://3.219.123.15:9000/admin/save_streamlit_media/image"
    data = {
        "url": image_url,
        "prompt": prompt
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_replicate_data(token):
    url = "http://3.219.123.15:9000/admin/get_streamlit_media"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except:
        return {'data':{}}

def save_replicate_video(video_url, token, prompt, max_frames):
    url = "http://3.219.123.15:9000/admin/save_streamlit_media/video"
    data = {
        "url": video_url,
        "prompt": prompt,
        "max_frames": max_frames
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_transcript(id: str):
    results_endpoint = "https://api.assemblyai.com/v2/transcript/{}".format(id)
    headers = {
        "Authorization": st.secrets['ASSEMBLYAI_KEY']
    }

    response = requests.get(results_endpoint, headers=headers)
    res = response.json()
    return res

def generate_audiogram(quotes, font, font_color, audio_url, video_url, token, audio_ext, font_size):
    url = "http://3.219.123.15:9999/admin/audiogram"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "quotes": quotes,
        "font": font,
        "font_color": font_color,
        "audio_url": audio_url,
        "video_url": video_url,
        "audio_ext": audio_ext,
        "font_size": font_size
    }
    response = requests.post(url, json=data, headers=headers)
    # Read response body as bytes
    res = response.content
    return res

def process_into_smaller_chunks_for_editing(data, pause_threshold=50):
    """Divides transcript output from assembly.ai into smaller chunks for editing.
    Division of chunks is based on speaker change, audio pauses, and audio breaks.
    Change pause threshold to vary chunk size.
    """
    utt = data['utterances']
    text = data['text']
    transcript = []
    for u in utt:
        speaker_tag = u['speaker']
        words = u['words']
        curr_utt = []
        for i in range(len(words)):
            if i == 0:
                curr_utt.append(words[i])
                continue
            else:
                pause_time = words[i]['start'] - words[i-1]['end']
                text = [w['text'] for w in curr_utt]
                text = " ".join(text)
                if pause_time > pause_threshold and ("." in words[i-1]['text'] or "?" in words[i-1]['text'] or "!" in words[i-1]['text']) and len(text) > 200:
                    text = [w['text'] for w in curr_utt]
                    text = " ".join(text)
                    start_time = curr_utt[0]['start']
                    timestamp = str(timedelta(seconds=int(start_time/1000)))
                    curr_utt_data = {
                        "speaker": speaker_tag,
                        "text": text,
                        "start": timestamp
                    }
                    text = [w['text'] for w in curr_utt]
                    text = " ".join(text)
                    start_time = curr_utt[0]['start']
                    end_time = curr_utt[-1]['end']
                    start_timestamp = str(timedelta(seconds=int(start_time/1000)))
                    end_timestamp = str(timedelta(seconds=int(end_time/1000)))
                    formatted_curr_utt = []
                    for c in curr_utt:
                        c['start_timestamp'] = str(timedelta(seconds=int(c['start']/1000)))
                        c['end_timestamp'] = str(timedelta(seconds=int(c['end']/1000)))
                        formatted_curr_utt.append(c)
                    curr_utt_data = {
                        "speaker": speaker_tag,
                        "text": text,
                        "start_timestamp": start_timestamp,
                        "start": start_time,
                        "end_timestamp": end_timestamp,
                        "end": end_time,
                        "words": curr_utt
                    }
                    transcript.append(curr_utt_data)
                    curr_utt = []
                curr_utt.append(words[i])
        if curr_utt:
            text = [w['text'] for w in curr_utt]
            text = " ".join(text)
            start_time = curr_utt[0]['start']
            end_time = curr_utt[-1]['end']
            start_timestamp = str(timedelta(seconds=int(start_time/1000)))
            end_timestamp = str(timedelta(seconds=int(end_time/1000)))
            formatted_curr_utt = []
            for c in curr_utt:
                c['start_timestamp'] = str(timedelta(seconds=int(c['start']/1000)))
                c['end_timestamp'] = str(timedelta(seconds=int(c['end']/1000)))
                formatted_curr_utt.append(c)
            curr_utt_data = {
                "speaker": speaker_tag,
                "text": text,
                "start_timestamp": start_timestamp,
                "start": start_time,
                "end_timestamp": end_timestamp,
                "end": end_time,
                "words": curr_utt
            }
            transcript.append(curr_utt_data)
    return transcript