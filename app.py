import io
import time
import streamlit as st
import deciphr_api as deciphr
import replicate_api as replicate
import requests
from genre import genre as all_genres
import datetime
from collections import namedtuple
import re
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import json
from fonts import ALL_FONTS

st.set_page_config(page_title="Deciphr Admins", page_icon=":rocket:")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] > .main {
animation-name: gradient;
background: linear-gradient(-45deg, #000000, #4c0089, #001c90);
background-size: 200% 100%;
animation: gradient 15s ease infinite;
animation-duration: 60s;
}
@keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}
[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
right: 2rem;
}
[data-testid="stExpander"]{
background-color: #0c0c0c;
border-radius: 5px;
box-shadow: 10px 10px 30px 2px #000000;
}
[id="body"]
{
    background: rgba(0, 0, 0, 0.1);
}
</style>
"""
        
st.markdown(page_bg_img, unsafe_allow_html=True)


if "token" not in st.session_state:
    st.session_state.token = None
    
if "display_name" not in st.session_state:
    st.session_state.display_name = None
    
if "user_email" not in st.session_state:
    st.session_state.user_email = None
    
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    
if "logged_in_flag" not in st.session_state:
    st.session_state.logged_in_flag = False
    
if "curr_file_id" not in st.session_state:
    st.session_state.curr_file_id = None
    
if "curr_file_data" not in st.session_state:
    st.session_state.curr_file_data = None
    
if "curr_file_quotes" not in st.session_state:
    st.session_state.curr_file_quotes = None
    
if "image_generation_dashboard" not in st.session_state:
    st.session_state.image_generation_dashboard = None
    
if "animation_generation_dashboard" not in st.session_state:
    st.session_state.animation_generation_dashboard = None
    
if "animation_get_url" not in st.session_state:
    st.session_state.animation_get_url = None
    
if "search_listen_notes_dashboard" not in st.session_state:
    st.session_state.search_listen_notes_dashboard = None
    
if "search_listen_notes_results" not in st.session_state:
    st.session_state.search_listen_notes_results = None
    
if "search_listen_notes_page_offset" not in st.session_state:
    st.session_state.search_listen_notes_page_offset = 0
    
if "selected_listen_notes_result" not in st.session_state:
    st.session_state.selected_listen_notes_result = None
    
if "curr_promt_image" not in st.session_state:
    st.session_state.curr_promt_image = None

if "curr_promt_video" not in st.session_state:
    st.session_state.curr_promt_video = None
    
if "set_email_verification_flag" not in st.session_state:
    st.session_state.set_email_verification_flag = None
    
if "prospective_process_status" not in st.session_state:
    st.session_state.prospective_process_status = None
    
if "prospective_process_id" not in st.session_state:
    st.session_state.prospective_process_id = None
    
if "user_records" not in st.session_state:
    st.session_state.user_records = None
    
if "last_day_new_users" not in st.session_state:
    st.session_state.last_day_new_users = None
    
if "verified_users" not in st.session_state:
    st.session_state.verified_users = None

if "download_content" not in st.session_state:
    st.session_state.download_content = None
    
if "download_format" not in st.session_state:
    st.session_state.download_format = None
    
if "replicate_data" not in st.session_state:
    st.session_state.replicate_data = None
    
if "replicate_video_buffer" not in st.session_state:
    st.session_state.replicate_video_buffer = {}
    
if "set_audiogram_flag" not in st.session_state:
    st.session_state.set_audiogram_flag = None
    
if "audiogram_transcript_file" not in st.session_state:
    st.session_state.audiogram_transcript_file = None
    
if "audiogram_file_data" not in st.session_state:
    st.session_state.audiogram_file_data = None
    
if "audiogram_chunked_transcript" not in st.session_state:
    st.session_state.audiogram_chunked_transcript = None
    
if "selected_audiogram_utterances" not in st.session_state:
    st.session_state.selected_audiogram_utterances = []
    
if "audiogram_video_url" not in st.session_state:
    st.session_state.audiogram_video_url = None
    
if "audiogram_video_output" not in st.session_state:
    st.session_state.audiogram_video_output = None
    
    
listen_notes_data = namedtuple('listen_notes_data', ['query', 'sort_by', 'type_', 'min_len', 'max_len', 'genre', 'published_before', 'publised_after', 'only_in'])

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets1.lottiefiles.com/packages/lf20_9zddpfah.json"
lottie_json = load_lottieurl(lottie_url)

def header():
    st.title("")
    st.title("")
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    with st.container():
        cols = st.columns([0.2,1,0.2])
        cols[0].write("")
        cols[1].image("https://api.deciphr.ai/static/deciphr-logo")
        cols[2].write("")
    st.write("---")
    
def login_container():
    with st.container():
        cols = st.columns([0.2,1,0.2])
        cols[0].text("")
        cols[2].text("")
        cols[1].subheader("Login")
        email = cols[1].text_input("Email")
        password = cols[1].text_input("Password", type="password")
        cols[1].button("Login", on_click=login_user, args=(email, password))
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
def login_user(email, password):
    with st.spinner("Logging in..."):
        response = deciphr.login(email, password)
        if 'token' in response and 'role' in response and response['role'] == 'ADMIN':
            st.session_state.token = response['token']
            st.session_state.display_name = response['user']['displayName']
            st.session_state.user_email = response['user']['email']
            st.session_state.user_id = response['user']['localId']
            st.session_state.logged_in_flag = True
            st.success("Logged in!")
            st.info("Welcome, {}!".format(st.session_state.display_name))
        else:
            try:
                st.error("{}".format(response['message']))
            except:
                st.error("Access denied. Contact admin for permission.")
            
def logout_user():
    st.session_state.logged_in_flag = False
    
def set_email_verification_flag():
    st.session_state.set_email_verification_flag = True
    
def set_review_flag():
    st.session_state.set_review_flag = True
    
def set_audiogram_flag():
    st.session_state.set_audiogram_flag = True
            
def dashboard():
    st.title("Dashboard")
    st.info("Hi, \n Just wanted to say a big thank you for taking the time to participate in the review poll.")
    st.info("UPDATES:")
    st.info("User Generated Image and Animation files are now saved in the database. You can view and download them from the 'Image Generation' or 'Animation' tab.")
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.subheader("Your Transcripts")
    
    with st.sidebar:
        st.header("Miscaellaneous")
        st.button("1: Image Generation", on_click=set_generate_image_flag)
        st.button("2: Animation", on_click=set_generate_animation_flag)
        st.button("3: Audiogram", on_click=set_audiogram_flag)
        st.write("---")
        # st.header("Prospective User")
        # st.button("1: Search ListenNotes", on_click=set_search_listen_notes_flag)
        # st.write("---")
        # st.header("Admin")
        # st.button("Email Verification", on_click=set_email_verification_flag)
        # st.button("Review", on_click=set_review_flag)
    
    n = 4
    user_transcripts = deciphr.get_user_transcripts(st.session_state.token)
    user_transcripts_chunked = [user_transcripts[i * n:(i + 1) * n] for i in range((len(user_transcripts) + n - 1) // n )]
    for transcripts in user_transcripts_chunked:
        with st.container():
            cols = st.columns([1,1,1,1])
            index = 0
            for transcript in transcripts:
                with cols[index].expander((transcript['title'][0:15]+"...").replace(" ", "_"), expanded=True):
                    st.write("Uploaded Date: ", transcript['display_datetime'])
                    st.write("---")
                    st.button("View File", key = transcript['id'], on_click=set_curr_vewing_file_id, args=(transcript['id'],))
                index += 1
            st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
            
    st.subheader("Your Audio Files")
    
    user_audio = deciphr.get_user_audio(st.session_state.token)
    user_audio_chunked = [user_audio[i * n:(i + 1) * n] for i in range((len(user_audio) + n - 1) // n )]
    prospective_files = []
    for transcripts in user_audio_chunked:
        with st.container():
            cols = st.columns([1,1,1,1])
            index = 0
            for transcript in transcripts:
                if "prospective" in transcript:
                    prospective_files.append(transcript)
                    continue
                try:
                    title = (transcript['title'][0:15]+"...").replace(" ", "_")
                except:
                    title = "Untitled_Audio"
                with cols[index].expander(title, expanded=True):
                    st.write("Uploaded Date: ", transcript['display_datetime'])
                    st.write("---")
                    st.button("View File", key = transcript['id'], on_click=set_curr_vewing_file_id, args=(transcript['id'],))
                index += 1
            st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
    # st.subheader("Listen Notes Audio Files")
    # prospective_files = [prospective_files[i * n:(i + 1) * n] for i in range((len(prospective_files) + n - 1) // n )]
    # for transcripts in prospective_files:
    #     with st.container():
    #         cols = st.columns([1,1,1,1])
    #         index = 0
    #         for transcript in transcripts:
    #             try:
    #                 title = (transcript['title'][0:15]+"...").replace(" ", "_")
    #             except:
    #                 title = "Untitled_Audio"
    #             with cols[index].expander(title, expanded=True):
    #                 st.write("Uploaded Date: ", transcript['display_datetime'])
    #                 st.write("---")
    #                 st.button("View File", key = transcript['id']+str(transcript['unix']), on_click=set_curr_vewing_file_id, args=(transcript['id'],))
    #             index += 1
    #         st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)

            

def set_generate_image_flag():
    st.session_state.image_generation_dashboard = True
    
def set_generate_animation_flag():
    st.session_state.animation_generation_dashboard = True
    
def set_search_listen_notes_flag():
    st.session_state.search_listen_notes_dashboard = True
    
def image_generation_dashboard():
    st.write("---")
    st.info("Click here to go back to your dashboard.")
    st.button("Back", on_click=reset_file_attributes)
    st.header("Image Generation")
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.info("Tips for writing prompts!")
    st.caption('- Be As Specific as You Can.')
    st.caption('- Name Specific Art Styles or Mediums.')
    st.caption('- Name Specific Artists to Guide Stable Diffusion.')
    st.caption('- Reference The Example Prompt given Below.')
    st.write("---")
    st.session_state.replicate_data = deciphr.get_replicate_data(st.session_state.token)['data']
    prompt = st.text_area("Enter Your Prompt Here", height=150, value="A grand city in the year 2100, atmospheric, hyper realistic, 8k, epic composition, cinematic, octane render, artstation landscape vista photography by Carr Clifton & Galen Rowell, 16K resolution, Landscape veduta photo by Dustin Lefevre & tdraw, 8k resolution, detailed landscape painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, Breath of The Wild, 4k detailed post processing, artstation, rendering by octane, unreal engine")
    st.subheader("Hyper Parameters")
    width = st.selectbox("Width", [512, 768], index = 0)
    height = st.selectbox("Height", [512, 768], index = 0)
    inference_step = st.number_input("Number of Inference Steps", value=100, min_value=50, max_value=200, help="Number of denoising steps. Higher values will result in more detailed images, but will take longer to generate.")
    # init_image = st.text_input("Enter image url to perform Image to Image generation")
    init_image = None
    if st.button("Submit"):
        if not prompt:
            st.error("Please enter a prompt.")
        else:
            with st.spinner('Processing Prompt...'):
                if init_image:
                    res = replicate.image_to_image(prompt, init_image)
                else:
                    res = replicate.generate_image_v2(prompt, width, height, inference_step)
                st.session_state.curr_promt_image = res
                deciphr.save_replicate_image(res, st.session_state.token, prompt)
                st.session_state.replicate_data = deciphr.get_replicate_data(st.session_state.token)['data']
    if st.session_state.curr_promt_image:
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        with st.container():
            cols = st.columns([1,5,1])
            cols[0].write()
            cols[1].image(st.session_state.curr_promt_image)
            # Download image
            response = requests.get(st.session_state.curr_promt_image)
            image_bytes = io.BytesIO(response.content)
            btn = cols[1].download_button(
                                        label="Download Image",
                                        data=image_bytes,
                                        file_name="deciphr_stable_diffusion.png",
                                        mime="image/png"
                                    )
            cols[2].write()
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
    st.header("Your Files")
    st.write("---")
    with st.container():
        cols = st.columns([1,1])
        curr_col = 0
        if 'images' in st.session_state.replicate_data:
            for index,item in enumerate(st.session_state.replicate_data['images']):
                with cols[curr_col].expander(f"Image {index+1}", expanded=True):
                    date_time = datetime.datetime.fromtimestamp(item['unix']/1000)
                    date_time = date_time.strftime("%d-%m-%Y %H:%M")
                    st.image(item['url'])
                    st.write("---")
                    st.caption(f"Date: {date_time}")
                    st.caption(f"Prompt: {item['prompt']}")
                    st.write("---")
                    response = requests.get(item['url'])
                    image_bytes = io.BytesIO(response.content)
                    st.download_button(
                                        label="Download Image",
                                        data=image_bytes,
                                        file_name=f"deciphr_stable_diffusion_{index}.png",
                                        mime="image/png"
                                    )
                curr_col += 1
                if curr_col == 2:
                    curr_col = 0
        else:
            st.info("Generate Images to see them here.")
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
                
        
def animation_generation_dashboard():
    st.write("---")
    st.info("Click here to go back to your dashboard.")
    st.button("Back", on_click=reset_file_attributes)
    st.header("Animations")
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.info("Tips for writing prompts!")
    st.write('- Be As Specific as You Can.')
    st.write('- Name Specific Art Styles or Mediums.')
    st.write('- Name Specific Artists to Guide Stable Diffusion.')
    st.write('- Provide \'frame number : prompt at this frame\', separate different prompts with \'|\'. Make sure the frame number does not exceed 100.')
    st.write('- End prompts with \'trending on ArtStation\' this seems to make the results better in my opinion(doesn\'t always).')
    st.write('- Reference The Example Prompt given Below.')
    st.write("---")
    st.session_state.replicate_data = deciphr.get_replicate_data(st.session_state.token)['data']
    prompt = st.text_area("Enter Your Prompt Here", height=150, value="0: a beautiful apple, trending on Artstation | 33: a beautiful banana, trending on Artstation | 66: a beautiful coconut, trending on Artstation | 100: a beautiful durian, trending on Artstation")
    max_frames = st.number_input("Number of Frames", min_value=100, max_value=500, value=100)
    fps = st.slider("FPS", min_value=10, max_value=30, value=15)
    st.write("---")
    if st.button("Submit"):
        if not prompt:
            st.error("Please enter a prompt.")
        else:
            status_text = 'Processing Prompt...'
            with st.spinner(status_text):
                st.session_state.animation_get_url = replicate.generate_video(prompt, max_frames, fps)
                deciphr.save_replicate_video(st.session_state.animation_get_url, st.session_state.token, prompt, max_frames)
                st.session_state.replicate_data = deciphr.get_replicate_data(st.session_state.token)['data']
                status, frames_complete, output, logs = replicate.video_results(st.session_state.animation_get_url)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
    st.header("Your Files")
    st.write("---")
    with st.container():
        cols = st.columns([1,1])
        curr_col = 0
        if 'videos' in st.session_state.replicate_data:
            for index,item in enumerate(st.session_state.replicate_data['videos']):
                with cols[curr_col].expander(f"Video {index+1}", expanded=True):
                    date_time = datetime.datetime.fromtimestamp(item['unix']/1000)
                    date_time = date_time.strftime("%d-%m-%Y %H:%M")
                    if item['url'] not in st.session_state.replicate_video_buffer:
                        status, frames_complete, output, logs = replicate.video_results(item['url'])
                        if status == "succeeded":
                            st.session_state.replicate_video_buffer[item['url']] = output
                    else:
                        output = st.session_state.replicate_video_buffer[item['url']]
                        status = "succeeded"
                    if status == "succeeded":
                        st.video(output)
                    else:
                        st.header(status.upper())
                        st_lottie(lottie_json)
                        my_bar = st.progress(0)
                        while status != "succeeded":
                            time.sleep(4)
                            status, frames_complete, output, logs = replicate.video_results(item['url'])
                            my_bar.progress(int((frames_complete/item['max_frames'])*100))
                            if status == "failed":
                                st.error("Error")
                                break
                            if status == "succeeded":
                                st.session_state.replicate_video_buffer[item['url']] = output
                                st.experimental_rerun()
                    st.write("---")
                    st.caption(f"Date: {date_time}")
                    st.caption(f"Prompt: {item['prompt']}")
                    st.write("---")
                    if status == "succeeded":
                        response = requests.get(output)
                        image_bytes = io.BytesIO(response.content)
                        st.download_button(
                                            label="Download Video",
                                            data=image_bytes,
                                            file_name=f"deciphr_stable_diffusion_{index}.mp4",
                                            mime="video/mp4",
                                            key=index
                                        )
                curr_col += 1
                if curr_col == 2:
                    curr_col = 0
        else:
            st.info("Generate Videos to see them here.")
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
    
def set_curr_vewing_file_id(id):
    st.session_state.curr_file_id = id
    
def view_file():
    st.write("---")
    st.info("Click here to go back to your dashboard.")
    st.button("Back", on_click=reset_file_attributes)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    if st.session_state.curr_file_data is None:
        file_data = deciphr.get_file_data(st.session_state.token, st.session_state.curr_file_id)
    else:
        file_data = st.session_state.curr_file_data
    if "error" not in file_data:
        st.session_state.curr_file_data = file_data
        headline = (file_data['es_doc']['headline']).strip().upper()
        audio_url = ""
        if 'serving_url' in file_data['fb_doc']:
            audio_url = file_data['fb_doc']['serving_url']
        if headline[-1] != ".":
            headline += "."
        st.header(headline)
        st.caption("File Name: {}".format(file_data['fb_doc']['title']))
        st.caption("Upload Date: {}".format(file_data['fb_doc']['display_datetime']))
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        if audio_url:
            st.audio(audio_url)
            st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        st.subheader("Abstract")
        st.write(file_data['es_doc']['abstract'])
        st.write("---")
        st.subheader("Transcript")
        download_transcript_contents = ""
        with st.expander("Transcript"):
            try:
                for t in file_data['es_doc']['display_transcript']:
                    line = f"{t['timestamp']} {t['speaker']}: {t['text']}"
                    st.caption(line)
                    download_transcript_contents += line + "\n\n"
            except:
                for t in file_data['es_doc']['display_transcript']:
                    st.caption(t)
                    download_transcript_contents += t + "\n\n"
        insights_download_contents = ""
        for i in file_data['es_doc']['insight']:
            insights_download_contents += i['timestamp']+" :"+ i['summary'] + "\n\n"
            
        download_transcript_contents = file_data['fb_doc']['title'] + "\n\n" +"ABSTRACT"+"\n\n" +file_data['es_doc']['abstract'] +"\n\n"+"TIMESTAMPS"+"\n\n"+insights_download_contents+"\n\n"+ "TRANSCRIPT"+"\n\n"+download_transcript_contents
        with st.container():
            cols = st.columns([1,1,1])
            cols[0].button('Download Transcript .txt', on_click=download_as_format, args=(st.session_state.curr_file_id, 'txt', st.session_state.token))
            cols[1].button('Download Transcript .docx', on_click=download_as_format, args=(st.session_state.curr_file_id, 'docx', st.session_state.token))
            cols[2].button('Download Transcript .pdf', on_click=download_as_format, args=(st.session_state.curr_file_id, 'pdf', st.session_state.token))

        if st.session_state.download_content:
            st.info(f"Your {st.session_state.download_format} file is ready. Click the button below to download.")
            st.download_button('Download Transcript', st.session_state.download_content, '{}_Transcript.{}'.format(file_data['fb_doc']['title'], st.session_state.download_format))
        
        st.write("---")
        st.subheader("Insights")
        with st.expander("Insights"):
                for i in file_data['es_doc']['insight']:
                    with st.container():
                        cols = st.columns([1.5,10])
                        cols[0].caption(i['timestamp']+" :")
                        cols[1].caption(i['summary'])
                    st.write("---")
        st.write("---")
        st.subheader("Key Quotes")
        st.caption("Note! These quotes are extracted using the current production model. Click on the \'Generate\' button below to generate new quotes using upgraded pipeline.")
        for q in file_data['es_doc']['key_quotes']:
            if type(q) == list:
                st.info(q[1])
            else:
                st.info(q)

        # if st.button("Generate"):
        #     st.write("---")
        #     if st.session_state.curr_file_quotes is None:
        #         with st.spinner("Extracting new quotes..."):
        #             quotes = deciphr.get_quotes(st.session_state.token, st.session_state.curr_file_id)
        #             st.session_state.curr_file_quotes = quotes
        #             st.success("Quotes generated!")
        #             st.balloons()

        if st.session_state.curr_file_quotes is not None:
            st.write("---")
            st.subheader("New Quotes")
            for nq in st.session_state.curr_file_quotes['data']:
                st.info("\""+nq[1]+"\"")
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)

def download_as_format(file_id, format, token):
    with st.spinner("Generating {} file...".format(format)):
        st.session_state.download_content = deciphr.download_file(file_id, format, token)
        st.session_state.download_format = format
        
   
def listen_notes_dashboard():
    st.write("---")
    st.info("Click here to go back to your dashboard.")
    st.button("Back", on_click=reset_file_attributes)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.header("Listen Notes")
    with st.expander("Better Search"):
        st.write("---")
        st.write("- Search results from ListenNotes API are different from searches done directly from listennotes.com")
        st.write("- For better search results and better functionality use listennotes.com to search for podcasts.")
        st.write("- Follow the steps below to get the podcast audio link from listennotes.com")
        st.write("- Paste the podcast audio link below to process the audio through Deciphr.")
        st.write("---")
        url = st.text_input("Podcast Audio Link", value="", key="podcast_id")
        if st.button('Process'):
            podcast_uid = re.findall(r'(?<=https://www.listennotes.com/e/)\w*', url)
            if podcast_uid:
                podcast_audio_url = f'https://www.listennotes.com/e/p/{podcast_uid[0]}'
                select_listen_notes_result(podcast_audio_url)
                st.experimental_rerun()
            else:
                st.error("Invalid podcast audio link. Please check the link and try again.")
        st.write("---")
        st.subheader('Steps:')
        st.write("- Search for a podcast on listennotes.com.")
        st.write("- Click on the podcast you want to process.")
        st.write("- Click on play button to start playing the podcast.")
        st.write("- Right click on the podcast image displayed on the audio player on the bottom of the screen and copy the link address.")
        st.write("- The link should look something like this: https://www.listennotes.com/e/ed98418381844b6b9e10c775ca8d2ae3")
        st.write("- Paste the link in the above text box and click on the \'Process\' button.")
        st.write("---")
        
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    all_genres_list = ['All'] + [i['name'] for i in all_genres['results']['genres']]
    query = st.text_input("Query")
    sort_by = st.selectbox("Sort By", ["Date", "Relevence"], index=0)
    type_ = st.selectbox("Type", ["Episode", "Podcast", "Curated"], index=0)
    min_len = st.number_input("Minimum Audio Length in Minutes", min_value=5, max_value=240, value=10)
    max_len = st.number_input("Maximum Audio Length in Minutes", min_value=5, max_value=440, value=240)
    genre = st.multiselect("Genre", all_genres_list, default=["All"])
    published_before = st.date_input("Published Before", datetime.date.today())
    publised_after = st.date_input("Published After", datetime.date(2000, 1, 1))
    only_in = st.multiselect("Only In", ["Title", "Description", "Author", "Audio"], default=["Title", "Description", "Author", "Audio"])
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    resp = None
    if st.button("Search"):
        if not query:
            st.error("Please enter a query.")
        else:
            ln_data = listen_notes_data(query, sort_by, type_, min_len, max_len, genre, published_before, publised_after, only_in)
            f_data = format_listen_notes_data(ln_data)
            resp = deciphr.search_listennotes(f_data.query, 
                                            f_data.sort_by, 
                                            f_data.type_, 
                                            f_data.min_len, 
                                            f_data.max_len, 
                                            f_data.genre, 
                                            f_data.published_before, 
                                            f_data.publised_after, 
                                            f_data.only_in, 
                                            st.session_state.token,)
            st.session_state.search_listen_notes_results = resp
            listen_notes_query_data = namedtuple('listen_notes_query_data', ['query', 'sort_by', 'type_', 'min_len', 'max_len', 'genre', 'published_before', 'publised_after', 'only_in'])
            st.session_state.search_listen_notes_page_offset = st.session_state.search_listen_notes_results['results']['next_offset']
        
    if st.session_state.search_listen_notes_results:
        display_listen_notes_results(st.session_state.search_listen_notes_results)
        

def format_listen_notes_data(data):
    all_genre_dict = {i['name']:i['id'] for i in all_genres['results']['genres']}
    query = '&'.join(data.query.split())
    published_before = (data.published_before - datetime.date(1970, 1, 1)) / datetime.timedelta(seconds=1)
    publised_after = (data.publised_after - datetime.date(1970, 1, 1)) / datetime.timedelta(seconds=1)
    genre = '' if 'All' in data.genre else ','.join([str(id) for name, id in all_genre_dict.items() if name in data.genre])
    only_in = ','.join([i.lower() for i in data.only_in])
    sort_by = data.sort_by.lower()
    return_data = listen_notes_data(query, sort_by, data.type_, data.min_len, data.max_len, genre, published_before, publised_after, only_in)
    return return_data
    
    
def display_listen_notes_results(resp):
    for res in resp['results']['results']:
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        with st.expander("", expanded=True):
            with st.container():
                cols = st.columns([4,10])
                pd_title = res['podcast']['title_original']
                episode_title = res['title_original']
                desc = res['description_original']
                image = res['podcast']['image']
                audio_url = res['audio']
                author = res['podcast']['publisher_original']
                cols[1].subheader(pd_title)
                cols[1].write(episode_title)
                cols[1].caption(f'By {author}')
                cols[0].subheader("...")
                cols[0].image(image)
                cols[1].audio(audio_url)
                cols[1].write("---")
                cols[1].button("Select", key=res['id'], on_click=select_listen_notes_result, args=(res,))
            
def listen_notes_processing_dashboard():
    st.write("---")
    st.info("Click here to go back")
    st.button("Back", on_click=back_to_listen_notes_dashboard)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.header("Process Audio")
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    audio_url = ""
    try:
        pd_title = st.session_state.selected_listen_notes_result['podcast']['title_original']
        episode_title = st.session_state.selected_listen_notes_result['title_original']
        desc = st.session_state.selected_listen_notes_result['description_original']
        image = st.session_state.selected_listen_notes_result['podcast']['image']
        audio_url = st.session_state.selected_listen_notes_result['audio']
        author = st.session_state.selected_listen_notes_result['podcast']['publisher_original']
        st.title(pd_title)
        st.image(image)
        st.subheader(episode_title)
        st.caption(f'By {author}')
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        st.subheader("Description")
        st.markdown(desc, unsafe_allow_html=True)
        st.write("---")
        st.audio(audio_url)
    except:
        audio_url = st.session_state.selected_listen_notes_result
        st.audio(audio_url)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.subheader("Select Start and End Timestamp")
    st.info("To process the entire audio, leave the start and end timestamp as is.")
    file_name = st.text_input("File Name")
    start_timestamp = st.text_input("Start Timestamp", value='00:00:00', key='start_timestamp')
    end_timestamp = st.text_input("End Timestamp", value='00:00:00', key='end_timestamp')
    if st.button("Process"):
        s_h, s_m, s_s = start_timestamp.split(":")
        e_h, e_m, e_s = end_timestamp.split(":")
        start = int(datetime.timedelta(hours=int(s_h),minutes=int(s_m),seconds=int(s_s)).total_seconds())*1000
        end = int(datetime.timedelta(hours=int(e_h),minutes=int(e_m),seconds=int(e_s)).total_seconds())*1000
        if not file_name:
            st.error("Please enter a file name")
        elif start >= end:
            if not(start == 0 and end == 0):
                st.error("Start timestamp must be less than end timestamp")
        else:
            process_prospective_audio(audio_url, file_name, start_timestamp, end_timestamp)
    if st.session_state.prospective_process_status and st.session_state.prospective_process_id:
        st.info(st.session_state.prospective_process_status)
        while st.session_state.prospective_process_status != "Completed":
            resp = deciphr.get_prospective_process_status(st.session_state.prospective_process_id, st.session_state.token)
            st.session_state.prospective_process_status = resp['fb_doc']['status']
            if 'processed' in resp['fb_doc'] and resp['fb_doc']['processed'] == 'Y':
                st.session_state.prospective_process_status = "Completed"
                st.success("Audio processed successfully")
                st.info("Check out the results on your dashboard!")
                st.balloons()
                break
            if 'error' in resp['fb_doc']:
                st.error(resp['fb_doc']['error'])
                break
            st.info(st.session_state.prospective_process_status)
            time.sleep(5)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
def process_prospective_audio(audio_url, file_name, start_timestamp, end_timestamp):
    resp = deciphr.prospective_user_process(file_name=file_name, start_timestamp=start_timestamp, end_timestamp=end_timestamp, audio_url=audio_url, token=st.session_state.token)
    if 'status' in resp and 'process_id' in resp:
        st.session_state.prospective_process_status = resp['status']
        st.session_state.prospective_process_id = resp['process_id']
    
        
        
def select_listen_notes_result(res):
    st.session_state.selected_listen_notes_result = res
    st.session_state.search_listen_notes_dashboard = False
    
def back_to_listen_notes_dashboard():
    st.session_state.search_listen_notes_dashboard = True
    st.session_state.selected_listen_notes_result = None
        
def email_verification_dashboard():
    st.write("---")
    st.info("Click here to go back")
    st.button("Back", on_click=reset_file_attributes)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    email = st.text_input("Enter User Email Address")
    st.button("Send Email Verification", on_click=send_email_verification, args=(email, st.session_state.token, ))
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    
def send_email_verification(email, token):
    resp = deciphr.send_email_verification(email, token)
    st.success(resp['message'])
    
    
def reset_file_attributes():
    st.session_state.curr_file_id = None
    st.session_state.curr_file_data = None
    st.session_state.curr_file_quotes = None
    st.session_state.image_generation_dashboard = None
    st.session_state.animation_generation_dashboard = None
    st.session_state.search_listen_notes_dashboard = None
    st.session_state.set_email_verification_flag = None
    st.session_state.set_audiogram_flag = None
    

def set_file_for_audiogram(transcript_id):
    st.session_state.audiogram_transcript_file = transcript_id

def audiogram_dashboard():
    st.write("---")
    st.info("Click here to go back")
    st.button("Back", on_click=reset_file_attributes)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.title("Audiogram")
    st.info("Audiograms can be generated for already transcribed audio files.")
    user_audio = deciphr.get_user_audio(st.session_state.token)
    if len(user_audio) == 0:
        st.error("No audio files found. Please upload an audio file through app.deciphr.ai")
    else:
        st.info("Please select a file to proceed")
        n = 4
        user_audio_chunked = [user_audio[i * n:(i + 1) * n] for i in range((len(user_audio) + n - 1) // n )]
        prospective_files = []
        for transcripts in user_audio_chunked:
            with st.container():
                cols = st.columns([1,1,1,1])
                index = 0
                for transcript in transcripts:
                    if "prospective" in transcript:
                        prospective_files.append(transcript)
                        continue
                    try:
                        title = (transcript['title'][0:15]+"...").replace(" ", "_")
                    except:
                        title = "Untitled_Audio"
                    with cols[index].expander(title, expanded=True):
                        st.write("Uploaded Date: ", transcript['display_datetime'])
                        st.write("---")
                        st.button("Select", key = transcript['id'], on_click=set_file_for_audiogram, args=(transcript['id'],))
                    index += 1
                st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)

def reset_audiogram_transcript_id():
    st.session_state.audiogram_transcript_file = None
    st.session_state.audiogram_file_data = None
    st.session_state.audiogram_chunked_transcript = None
    st.session_state.selected_audiogram_utterances = []
    
def append_audiogram_utterance(chunk, remove=False):
    if remove:
        st.session_state.selected_audiogram_utterances.remove(chunk)
    else:
        st.session_state.selected_audiogram_utterances.append(chunk)
        
def set_audiogram_video(url):
    st.session_state.audiogram_video_url = url

def audiogram_editor():
    st.write("---")
    st.info("Click here to go back")
    st.button("Back", on_click=reset_audiogram_transcript_id)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    if st.session_state.audiogram_file_data is None:
        st.session_state.audiogram_file_data = deciphr.get_file_data(st.session_state.token, st.session_state.audiogram_transcript_file)
    file_data = st.session_state.audiogram_file_data
    st.header(file_data['fb_doc']['title'])
    st.caption(file_data['fb_doc']['display_datetime'])
    st.write("---")
    st.header("Abstract")
    st.write(file_data['es_doc']['abstract'])
    st.write("---")
    if st.session_state.audiogram_chunked_transcript == None:
        transcript = deciphr.get_transcript(file_data['fb_doc']['assembly_id'])
        chunked_transcript = deciphr.process_into_smaller_chunks_for_editing(transcript)
        st.session_state.audiogram_chunked_transcript = chunked_transcript
    chunked_transcript = st.session_state.audiogram_chunked_transcript
    proceed = False
    if len(st.session_state.selected_audiogram_utterances) > 0:
        proceed = st.button("Proceed")
    if not proceed:
        st.header("Select one or more utterances")
        st.info(f"{len(st.session_state.selected_audiogram_utterances)} Selected")
        for index,chunk in enumerate(chunked_transcript):
            with st.expander(f"Utterance {index+1}", expanded=True):
                st.caption(f"{chunk['start_timestamp']} Speaker: {chunk['speaker']}")
                st.caption(chunk['text'])
                if chunk in st.session_state.selected_audiogram_utterances:
                    st.button("Deselect", key=index, on_click=append_audiogram_utterance, args=(chunk, True))
                else:
                    st.button("Select", key=index, on_click=append_audiogram_utterance, args=(chunk, ))
    else:
        st.header("Select a background video")
        with st.container():
            cols = st.columns([1,1])
            curr_col = 0
            st.session_state.replicate_data = deciphr.get_replicate_data(st.session_state.token)['data']
            if 'videos' in st.session_state.replicate_data:
                for index,item in enumerate(st.session_state.replicate_data['videos']):
                    with cols[curr_col].expander(f"Video {index+1}", expanded=True):
                        date_time = datetime.datetime.fromtimestamp(item['unix']/1000)
                        date_time = date_time.strftime("%d-%m-%Y %H:%M")
                        if item['url'] not in st.session_state.replicate_video_buffer:
                            status, frames_complete, output, logs = replicate.video_results(item['url'])
                            if status == "succeeded":
                                st.session_state.replicate_video_buffer[item['url']] = output
                        else:
                            output = st.session_state.replicate_video_buffer[item['url']]
                            status = "succeeded"
                        if status == "succeeded":
                            st.video(output)
                        else:
                            st.header(status.upper())
                            st_lottie(lottie_json)
                            my_bar = st.progress(0)
                            while status != "succeeded":
                                time.sleep(4)
                                status, frames_complete, output, logs = replicate.video_results(item['url'])
                                my_bar.progress(int((frames_complete/item['max_frames'])*100))
                                if status == "failed":
                                    st.error("Error")
                                    break
                                if status == "succeeded":
                                    st.session_state.replicate_video_buffer[item['url']] = output
                                    st.experimental_rerun()
                        st.caption(f"Date: {date_time}")
                        if status == "succeeded":
                            st.button(label="Select", key=index, on_click=set_audiogram_video, args=(output,))
                    curr_col += 1
                    if curr_col == 2:
                        curr_col = 0
            else:
                st.info("Generate Videos to see them here.")
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        
def reset_audiogram_video():
    st.session_state.audiogram_video_url = None

def customize_audiogram():
    st.write("---")
    st.info("Click here to go back")
    st.button("Back", on_click=reset_audiogram_video)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.header("Preview selected items")
    st.write("---")
    st.subheader("Selected Video")
    st.video(st.session_state.audiogram_video_url)
    st.write("---")
    st.subheader("Selected Utterances")
    for utt in st.session_state.selected_audiogram_utterances:
        st.caption(f"{utt['start_timestamp']} Speaker: {utt['speaker']}")
        st.caption(utt['text'])
    st.write("---")
    st.subheader("Audio")
    st.audio(st.session_state.audiogram_file_data["fb_doc"]["serving_url"])
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.header("Customize your Audiogram")
    st.info("Other customizations(branding and styling) will be added in the future...")
    font = st.selectbox("Font", ALL_FONTS)
    font_color = st.color_picker("Font Color")
    font_size = st.slider("Font Size", min_value=10, max_value=100, value=28)
    if st.button("Generate Audiogram"):
        with st.spinner("Generating Audiogram..."):
            generate_audiogram(font, font_color, font_size)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    if st.session_state.audiogram_video_output:
        st.header("Output")
        st.video(st.session_state.audiogram_video_output)
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        
    
def generate_audiogram(font, font_color, font_size):
    res = deciphr.generate_audiogram(quotes=st.session_state.selected_audiogram_utterances,
                                     font=font, 
                                     font_color=font_color, 
                                     audio_url=st.session_state.audiogram_file_data["fb_doc"]["serving_url"], 
                                     video_url=st.session_state.audiogram_video_url, 
                                     token=st.session_state.token,
                                     audio_ext=st.session_state.audiogram_file_data["fb_doc"]["path"].split(".")[-1],
                                     font_size=font_size)
    
    st.session_state.audiogram_video_output = res

    
if __name__ == "__main__":
    if not st.session_state.logged_in_flag:
        header()
        login_container()
    elif st.session_state.curr_file_id is not None:
        view_file()
    elif st.session_state.image_generation_dashboard:
        image_generation_dashboard()
    elif st.session_state.animation_generation_dashboard:
        animation_generation_dashboard()
    elif st.session_state.search_listen_notes_dashboard:
        listen_notes_dashboard()
    elif st.session_state.selected_listen_notes_result:
        listen_notes_processing_dashboard()
    elif st.session_state.set_email_verification_flag:
        email_verification_dashboard()
    elif st.session_state.set_audiogram_flag and not st.session_state.audiogram_transcript_file:
        audiogram_dashboard()
    elif st.session_state.audiogram_transcript_file and not st.session_state.audiogram_video_url:
        audiogram_editor()
    elif st.session_state.audiogram_video_url:
        customize_audiogram()
    else:
        dashboard()