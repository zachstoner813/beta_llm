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
file_paths = ["static_files/BAP AI Canadiate and Chapter Information.docx", "static_files/BAP AI National Policies and Produres.docx", "var_files/BAP_Schedule.docx"]

# Looking for exisiting thread ID
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = None


# Check if assistant already exists in the session state
#if 'assistant_id' not in st.session_state:
    # Upload files and create an assistant
#    file_ids = upload_files(client, file_paths)
#    assistant = create_assistant(client, file_ids)
#    st.session_state.assistant_id = assistant.id
#    st.session_state.file_ids = file_ids
def create_and_store_assistant():
    file_ids = upload_files(client, file_paths)
    assistant = create_assistant(client, file_ids)
    st.session_state['assistant_id'] = assistant.id
    st.session_state['file_ids'] = file_ids




# Streamlit layout for user input
st.title("BAP-GPT")
user_query = st.text_area("**Enter your Beta Alpha Psi related questions here:** *I have information on policies and procedures, upcoming events, officer/chair contact info and the Candidate Manual*", height=150)
submit_button = st.button("Submit")

def process_query(query):
    # Create the assistant if it does not exist in the session
    if 'assistant_id' not in st.session_state:
        file_ids = upload_files(client, file_paths)
        assistant = create_assistant(client, file_ids)
        st.session_state['assistant_id'] = assistant.id
        st.session_state['file_ids'] = file_ids

    # Check if this is the first query in the session
    if st.session_state['thread_id'] is None:
        st.session_state['thread_id'] = generate_response(client, query)
    else:
        generate_response(client, query, st.session_state['thread_id'])

    # Get the response from the assistant
    response = run_assistant(client, st.session_state['assistant_id'], st.session_state['thread_id'])
    return response


if submit_button and user_query:
    response = process_query(user_query)
    st.text_area("Response:", value=response, height=150, disabled=True)

def cleanup():
    if 'assistant_id' in st.session_state:
        # Delete assistant and any related resources here
        # ... [your code for deletion]
        del st.session_state['assistant_id']
        del st.session_state['file_ids']
        del st.session_state['thread_id']
    st.write("Assistant and resources have been cleaned up.")


# Add a new button for closing the app and deleting files..testtest,,
#if st.button('*CLICK ME when finished!*'):
#    for file_id in st.session_state.file_ids:
#        try:
#            file_deletion_status = client.beta.assistants.files.delete(
#                assistant_id=st.session_state.assistant_id,
#                file_id=file_id
#            )
#            print(f"File {file_id} deletion status: {file_deletion_status}")
#        except Exception as e:
#            print(f"Error deleting file {file_id}: {e}")
#    st.stop()  # Stop the Streamlit app
if st.button('*CLICK ME when finished!*'):
    cleanup()
    st.stop()  # Stop the Streamlit app