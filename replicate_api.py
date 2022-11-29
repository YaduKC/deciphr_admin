import os
import requests
import time
import re
import streamlit as st

REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

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

def generate_image_v2(prompt, width, height, inference_steps):
    headers = {
        'Authorization': f"Token {REPLICATE_API_TOKEN}",
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'version': 'c7fb9275bd443c22b69dfc6e253c7ca55dcb5787990d73304fb21e67eeff76e7',
        'input': {
            'prompt': prompt,
            'width': width,
            'height': height,
            'num_inference_steps': inference_steps,
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

def upscale_image(image_data):
    headers = {
        'Authorization': f"Token {REPLICATE_API_TOKEN}",
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'version': '660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a',
        'input': {
            'image': image_data,
        },
    }

    response = requests.post('https://api.replicate.com/v1/predictions', headers=headers, json=json_data)
    
    result = response.json()
    get_image_url = result['urls']['get']
    # get_image_url = 'https://api.replicate.com/v1/predictions/4mt2oppwerei3af3ftpvnl5ile'
    
    #get results
    resp = requests.get(get_image_url, headers=headers)
    print(resp.json())
    status = resp.json()['status']
    while status != 'succeeded':
        resp = requests.get(get_image_url, headers=headers)
        print(resp.json())
        
        status = resp.json()['status']
        time.sleep(4)
        if status == 'failed':
            return None
    
    output = resp.json()['output'][0]
    
    return output

def generate_video(prompt, max_frames=100, fps=15):
    headers = {
    'Authorization': f"Token {REPLICATE_API_TOKEN}",
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
    }

    json_data = {
        'version': 'e22e77495f2fb83c34d5fae2ad8ab63c0a87b6b573b6208e1535b23b89ea66d6',
        'input': {
            'max_frames': max_frames,
            'animation_prompts': prompt,
            'fps': fps
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
    print(resp.json())
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


def image_to_image(prompt, image_url):
    headers = {
        'Authorization': f"Token {REPLICATE_API_TOKEN}",
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'version': 'a9758cbfbd5f3c2094457d996681af52552901775aa2d6dd0b17fd15df959bef',
        'input': {
            'prompt': prompt,
            'prompt_strength' : 0.4,
            'init_image' : image_url,
            'guidance_scale' : "5",
            'num_inference_steps' : 100,
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
