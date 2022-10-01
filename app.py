from ast import arg
from email.mime import audio
import io
import time
from turtle import onclick
import streamlit as st
import deciphr_api as deciphr
import replicate_api as replicate
import requests
from genre import genre as all_genres
import datetime
from collections import namedtuple
import re
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
</style>
"""
def local_css(file_name="background.css"):
    with open(file_name) as f:
        style = f'<style>{f.read()}</style>'
        mk = """<div class="area" data-testid="stAppViewContainer">
            <ul class="circles">
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
                    <li></li>
            </ul>
    </div >"""
        # st.markdown(style+"\n"+mk, unsafe_allow_html=True)
        
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
    
listen_notes_data = namedtuple('listen_notes_data', ['query', 'sort_by', 'type_', 'min_len', 'max_len', 'genre', 'published_before', 'publised_after', 'only_in'])

    

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
    st.session_state.token = None
    st.session_state.display_name = None
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.session_state.logged_in_flag = False
    
def set_email_verification_flag():
    st.session_state.set_email_verification_flag = True
    
            
def dashboard():
    st.title("Dashboard")
    st.button("Logout", on_click=logout_user)
    st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
    st.subheader("Your Transcripts")
    
    with st.sidebar:
        st.header("Miscaellaneous")
        st.button("1: Image Generation", on_click=set_generate_image_flag)
        st.button("2: Animation", on_click=set_generate_animation_flag)
        st.write("---")
        st.header("Prospective User")
        st.button("1: Search ListenNotes", on_click=set_search_listen_notes_flag)
        st.write("---")
        st.header("Admin")
        st.button("Email Verification", on_click=set_email_verification_flag)
    
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
    
    st.subheader("Listen Notes Audio Files")
    prospective_files = [prospective_files[i * n:(i + 1) * n] for i in range((len(prospective_files) + n - 1) // n )]
    for transcripts in prospective_files:
        with st.container():
            cols = st.columns([1,1,1,1])
            index = 0
            for transcript in transcripts:
                try:
                    title = (transcript['title'][0:15]+"...").replace(" ", "_")
                except:
                    title = "Untitled_Audio"
                with cols[index].expander(title, expanded=True):
                    st.write("Uploaded Date: ", transcript['display_datetime'])
                    st.write("---")
                    st.button("View File", key = transcript['id']+str(transcript['unix']), on_click=set_curr_vewing_file_id, args=(transcript['id'],))
                index += 1
            st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)

            

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
    
    prompt = st.text_area("Enter Your Prompt Here", height=150, value="A grand city in the year 2100, atmospheric, hyper realistic, 8k, epic composition, cinematic, octane render, artstation landscape vista photography by Carr Clifton & Galen Rowell, 16K resolution, Landscape veduta photo by Dustin Lefevre & tdraw, 8k resolution, detailed landscape painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, Breath of The Wild, 4k detailed post processing, artstation, rendering by octane, unreal engine")
    if st.button("Submit"):
        if not prompt:
            st.error("Please enter a prompt.")
        else:
            with st.spinner('Processing Prompt...'):
                res = replicate.generate_image(prompt)
                st.session_state.curr_promt_image = res
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
    prompt = st.text_area("Enter Your Prompt Here", height=150, value="0: a beautiful apple, trending on Artstation | 33: a beautiful banana, trending on Artstation | 66: a beautiful coconut, trending on Artstation | 100: a beautiful durian, trending on Artstation")
    max_frames = st.number_input("Number of Frames", min_value=100, max_value=500, value=100)
    fps = st.slider("FPS", min_value=10, max_value=30, value=15)
    st.write("---")
    if st.button("Submit") or st.session_state.animation_get_url:
        if not prompt:
            st.error("Please enter a prompt.")
        else:
            status_text = 'Processing Prompt...'
            with st.spinner(status_text):
                st.session_state.animation_get_url = replicate.generate_video(prompt, max_frames, fps) if not st.session_state.animation_get_url else st.session_state.animation_get_url
                status, frames_complete, output, logs = replicate.video_results(st.session_state.animation_get_url)
                my_bar = st.progress(0)
                while status != "succeeded":
                    time.sleep(4)
                    status, frames_complete, output, logs = replicate.video_results(st.session_state.animation_get_url)
                    my_bar.progress(int((frames_complete/max_frames)*100))
                    if status == "failed":
                        st.error("Error")
                        st.write(logs)
                        break
                st.session_state.animation_get_url = None
                st.session_state.curr_promt_video = output
    if st.session_state.curr_promt_video:
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)
        with st.container():
            cols = st.columns([1,5,1])
            cols[0].write()
            cols[1].video(st.session_state.curr_promt_video)
            
            # Download video
            response = requests.get(st.session_state.curr_promt_video)
            image_bytes = io.BytesIO(response.content)
            btn = cols[1].download_button(
                                        label="Download Video",
                                        data=image_bytes,
                                        file_name="deciphr_deforum_stable_diffusion.mp4",
                                        mime="video/mp4"
                                    )
            cols[2].write()
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
            for t in file_data['es_doc']['display_transcript']:
                st.write(t)
                download_transcript_contents += t + "\n\n"
        st.download_button('Download Transcript', download_transcript_contents, '{}_Transcript.txt'.format(file_data['fb_doc']['title']))
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
            st.info(q)

        if st.button("Generate"):
            st.write("---")
            if st.session_state.curr_file_quotes is None:
                with st.spinner("Extracting new quotes..."):
                    quotes = deciphr.get_quotes(st.session_state.token, st.session_state.curr_file_id)
                    st.session_state.curr_file_quotes = quotes
                    st.success("Quotes generated!")
                    st.balloons()

        if st.session_state.curr_file_quotes is not None:
            st.write("---")
            st.subheader("New Quotes")
            for nq in st.session_state.curr_file_quotes['data']:
                st.info("\""+nq[1]+"\"")
        st.markdown("""<hr style="height:8px; background-color:#ffffff; border-radius:10px" /> """, unsafe_allow_html=True)

        
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
    

if __name__ == "__main__":
    local_css()
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
    else:
        dashboard()