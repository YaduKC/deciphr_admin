import io
import time
import streamlit as st
import deciphr_api as deciphr
import replicate_api as replicate
import requests

st.set_page_config(page_title="Deciphr Admins", page_icon=":rocket:")

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
    
if "curr_promt_image" not in st.session_state:
    st.session_state.curr_promt_image = None

if "curr_promt_video" not in st.session_state:
    st.session_state.curr_promt_video = None
    

def header():
    st.title("Deciphr")
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
    st.write("---")
    
def login_user(email, password):
    with st.spinner("Logging in..."):
        response = deciphr.login(email, password)
        if 'token' in response:
            st.session_state.token = response['token']
            st.session_state.display_name = response['user']['displayName']
            st.session_state.user_email = response['user']['email']
            st.session_state.user_id = response['user']['localId']
            st.session_state.logged_in_flag = True
            st.success("Logged in!")
            st.info("Welcome, {}!".format(st.session_state.display_name))
        else:
            st.error("{}".format(response['message']))
            
def logout_user():
    st.session_state.token = None
    st.session_state.display_name = None
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.session_state.logged_in_flag = False
            
def dashboard():
    st.header("Dashboard")
    st.button("Logout", on_click=logout_user)
    st.write("---")
    st.subheader("Your Transcripts")
    
    with st.sidebar:
        st.header("Miscaellaneous")
        st.write("---")
        st.button("1: Image Generation", on_click=set_generate_image_flag)
        st.button("2: Animation", on_click=set_generate_animation_flag)
    
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
            st.write("---")
            
    st.subheader("Your Audio Files")
    
    user_audio = deciphr.get_user_audio(st.session_state.token)
    user_audio_chunked = [user_audio[i * n:(i + 1) * n] for i in range((len(user_audio) + n - 1) // n )]
    for transcripts in user_audio_chunked:
        with st.container():
            cols = st.columns([1,1,1,1])
            index = 0
            for transcript in transcripts:
                with cols[index].expander((transcript['title'][0:15]+"...").replace(" ", "_"), expanded=True):
                    st.write("Uploaded Date: ", transcript['display_datetime'])
                    st.write("---")
                    st.button("View File", key = transcript['id'], on_click=set_curr_vewing_file_id, args=(transcript['id'],))
                index += 1
            st.write("---")
            

def set_generate_image_flag():
    st.session_state.image_generation_dashboard = True
    
def set_generate_animation_flag():
    st.session_state.animation_generation_dashboard = True
    
def image_generation_dashboard():
    st.write("---")
    st.info("Click here to go back to your dashboard.")
    st.button("Back", on_click=reset_file_attributes)
    st.header("Image Generation")
    st.write("---")
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
        st.write("---")
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
        st.write("---")
        
def animation_generation_dashboard():
    st.write("---")
    st.info("Click here to go back to your dashboard.")
    st.button("Back", on_click=reset_file_attributes)
    st.header("Animations")
    st.write("---")
    st.info("Tips for writing prompts!")
    st.caption('- Be As Specific as You Can.')
    st.caption('- Name Specific Art Styles or Mediums.')
    st.caption('- Name Specific Artists to Guide Stable Diffusion.')
    st.caption('- Provide \'frame number : prompt at this frame\', separate different prompts with \'|\'. Make sure the frame number does not exceed 100.')
    st.caption('- End prompts with \'trending on ArtStation\' this seems to make the results better in my opinion(doesn\'t always).')
    st.caption('- Reference The Example Prompt given Below.')
    st.write("---")
    prompt = st.text_area("Enter Your Prompt Here", height=150, value="0: a beautiful apple, trending on Artstation | 33: a beautiful banana, trending on Artstation | 66: a beautiful coconut, trending on Artstation | 100: a beautiful durian, trending on Artstation")
    if st.button("Submit"):
        if not prompt:
            st.error("Please enter a prompt.")
        else:
            status_text = 'Processing Prompt...'
            with st.spinner(status_text):
                get_url = replicate.generate_video(prompt)
                status, frames_complete, output, logs = replicate.video_results(get_url)
                my_bar = st.progress(0)
                while status != "succeeded":
                    time.sleep(4)
                    status, frames_complete, output, logs = replicate.video_results(get_url)
                    my_bar.progress(frames_complete)
                    if status == "failed":
                        st.error("Error")
                        break
                st.session_state.curr_promt_video = output
    if st.session_state.curr_promt_video:
        st.write("---")
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
        st.write("---")
    

def set_curr_vewing_file_id(id):
    st.session_state.curr_file_id = id
    
def view_file():
    st.write("---")
    st.info("Click here to go back to your dashboard.")
    st.button("Back", on_click=reset_file_attributes)
    st.write("---")
    if st.session_state.curr_file_data is None:
        file_data = deciphr.get_file_data(st.session_state.token, st.session_state.curr_file_id)
    else:
        file_data = st.session_state.curr_file_data
    if "error" not in file_data:
        st.session_state.curr_file_data = file_data
        headline = (file_data['es_doc']['headline']).strip().upper()
        if headline[-1] != ".":
            headline += "."
        st.header(headline)
        st.caption("File Name: {}".format(file_data['fb_doc']['title']))
        st.caption("Upload Date: {}".format(file_data['fb_doc']['display_datetime']))
        st.write("---")
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
                        cols = st.columns([1,10])
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
        st.write("---")
        
def reset_file_attributes():
    st.session_state.curr_file_id = None
    st.session_state.curr_file_data = None
    st.session_state.curr_file_quotes = None
    st.session_state.image_generation_dashboard = None
    st.session_state.animation_generation_dashboard = None

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
    else:
        dashboard()