import streamlit as st
import deciphr_api as deciphr

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

if __name__ == "__main__":
    if not st.session_state.logged_in_flag:
        header()
        login_container()
    elif st.session_state.curr_file_id is not None:
        view_file()
    else:
        dashboard()