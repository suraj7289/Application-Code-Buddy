import os
import streamlit as st
import shutil
from read_file_content import get_file_content
from agent import CodeChatAgent

current_dir = os.getcwd()
uploaded_file_directory = os.path.join(current_dir, "my_files")

st.set_page_config(page_title="Code Buddy", page_icon=":books:")
st.title('💬Chat with your Application Code')

if "conversation" not in st.session_state:
    st.session_state.conversation = None
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Initialize uploaded files list
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
    if os.path.exists(uploaded_file_directory):
        # remove the old files each time application is started
        shutil.rmtree(uploaded_file_directory)
    # create a directory to store the uploaded documents by user
    os.mkdir(uploaded_file_directory)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input(placeholder='Ask a question ?',
                                  # We used the := operator to assign the user's input to the prompt variable and checked if it's not None in the same line
                                  ):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_question)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # print(st.session_state.query_engine)
        CodeChatAgent = CodeChatAgent()
        assistant_response = CodeChatAgent.chat_messages(user_question)
        message_placeholder.markdown(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

with st.sidebar:
    st.subheader("Upload Application ZIP File", divider='rainbow')
    uploaded_file = st.file_uploader("Upload your ZIP file and click on 'Process'", type=['zip'])
    if uploaded_file is not None and uploaded_file.name not in st.session_state.uploaded_files:

        # if uploaded_file is not None:
        with st.spinner("Processing"):
            # Set path for the uploaded file
            uploaded_file_path = os.path.join(uploaded_file_directory,uploaded_file.name)
            print('uploaded_file_path: ',uploaded_file_path)
            # Save the uploaded file to the directory
            with open(uploaded_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            zip_text = get_file_content(uploaded_file_path)
            with open(os.path.join(uploaded_file_directory,"zip_file_text.txt"), 'w') as f:
                f.write(zip_text)



