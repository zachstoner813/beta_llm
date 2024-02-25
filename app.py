import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from assistant_creation import create_assistant
from file_upload import upload_files
from thread_management import generate_response, run_assistant

#st.secrets import
OPEN_AI_API_KEY = st.secrets["openai_secret_key"]
client = OpenAI(api_key=OPEN_AI_API_KEY)

# Paths to files to be uploaded
file_paths = ["static_files/BAP AI Canadiate and Chapter Information.docx", "static_files/BAP AI National Policies and Produres.docx", "var_files/BAP_sheet_data.docx"]

# Looking for exisiting thread ID
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = None


# Check if assistant already exists in the session state
if 'assistant_id' not in st.session_state:
    # Upload files and create an assistant
    file_ids = upload_files(client, file_paths)
    assistant = create_assistant(client, file_ids)
    st.session_state.assistant_id = assistant.id
    st.session_state.file_ids = file_ids

# Streamlit layout for user input
st.title("Beta Bot #23")
user_query = st.text_area("Enter your Beta Alpha Psi questions here:", height=150)
submit_button = st.button("Submit Query")

def process_query(query):
    if st.session_state['thread_id'] is None:
        st.session_state['thread_id'] = generate_response(client, query)
    else:
        generate_response(client, query, st.session_state['thread_id'])
    response = run_assistant(client, st.session_state.assistant_id, st.session_state['thread_id'])
    return response


# Existing code
if submit_button and user_query:
    response = process_query(user_query)
    st.text_area("Response:", value=response, height=150, disabled=True)

# Add a new button for closing the app and deleting files
if st.button('*CLICK ME when finished!*'):
    for file_id in st.session_state.file_ids:
        try:
            file_deletion_status = client.beta.assistants.files.delete(
                assistant_id=st.session_state.assistant_id,
                file_id=file_id
            )
            print(f"File {file_id} deletion status: {file_deletion_status}")
        except Exception as e:
            print(f"Error deleting file {file_id}: {e}")
    st.stop()  # Stop the Streamlit app
