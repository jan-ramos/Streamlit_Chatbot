import streamlit as st
from utils.html_blocks import bot_template, user_template, css
from dotenv import load_dotenv
from pptx import Presentation
import openai
import utils.chatflow as chat
import utils.auth as auth

st.set_page_config(page_title='Chat with your Notes', page_icon=':books:')

if auth.api_credentials():
    
    st.session_state['Query'] = False
    
    with st.sidebar:
        st.title("Upload your Notes Here: ")
        pdf_files = st.file_uploader("Choose your Notes Files and Press OK", accept_multiple_files=True)
        
        if len(pdf_files) > 0:
            st.session_state['Query'] = True
        else:
            st.session_state['chatbot-disabled'] = True
        
        if st.session_state['Query'] == True:
            if st.button("OK"):
                with st.spinner("Processing your Notes..."):
                            # Get PDF Text
                    raw_text = chat.document_loader(pdf_files)
                    if st.session_state['valid_file'] == True:
                        # Get Text Chunks
                        text_chunks = chat.split_text(raw_text)
                        
                        # Create Vector Store
                        vector_store = chat.vector_storage(text_chunks,openai.api_key)
                        st.success("Success!")
                        st.session_state['chatbot-disabled'] = False
                        st.session_state.conversation =  chat.get_conversation_chain(vector_store,openai.api_key)
                    
    st.write(css, unsafe_allow_html=True)
                
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
                
    st.header('📝 Ask a question to your AI-assistant')
    
        
    question = st.text_input("Type in question: ",disabled= st.session_state['chatbot-disabled'])

    if question:
        chat.handle_user_input(question)
