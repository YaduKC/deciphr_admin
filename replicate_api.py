import os
from config import REPLICATE_API_TOKEN
import requests
import time
import re
from dotenv import load_dotenv

load_dotenv('config.env')

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

def generate_image(prompt):
    headers = {
        'Authorization': f"Token {REPLICATE_API_TOKEN}",
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'version': 'a9758cbfbd5f3c2094457d996681af52552901775aa2d6dd0b17fd15df959bef',
        'input': {
            'prompt': prompt,
        },
    }

    response = requests.post('https://api.replicate.com/v1/predictions', headers=headers, json=json_data)
    
    result = response.json()
    get_image_url = result['urls']['get']
    # get_image_url = 'https://api.replicate.com/v1/predictions/4mt2oppwerei3af3ftpvnl5ile'
    
    #get results
    resp = requests.get(get_image_url, headers=headers)
    status = resp.json()['status']
    while status != 'succeeded':
        resp = requests.get(get_image_url, headers=headers)
        status = resp.json()['status']
        time.sleep(4)
    
    output = resp.json()['output'][0]
    
    return output

def generate_video(prompt):
    headers = {
    'Authorization': f"Token {REPLICATE_API_TOKEN}",
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
    }

    json_data = {
        'version': 'e22e77495f2fb83c34d5fae2ad8ab63c0a87b6b573b6208e1535b23b89ea66d6',
        'input': {
            'max_frames': 100,
            'animation_prompts': prompt,
            'fps': 15
        },
    }

    response = requests.post('https://api.replicate.com/v1/predictions', headers=headers, json=json_data)
    result = response.json()
    get_video_url = result['urls']['get']
    return get_video_url

def video_results(get_url):
    headers = {
    'Authorization': f"Token {REPLICATE_API_TOKEN}",
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
    }
    resp = requests.get(get_url, headers=headers)
    logs = resp.json()['logs']
    try:
        frames_complete = re.findall(r'Rendering animation frame \d+ of \d+', logs)[-1]
        frames_complete = int(frames_complete.split(' ')[-3])
    except:
        frames_complete = 0
    status = resp.json()['status']
    output_url = None
    if 'output' in resp.json():
        output_url = resp.json()['output']
    return status, frames_complete, output_url, logs
