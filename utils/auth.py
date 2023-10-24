import openai
import streamlit as st

def is_api_key_valid(key):
    if key == 'test':
        return True
    else:
        try:
             openai.api_key = key
             response = openai.Completion.create(
                engine="davinci",
                prompt="This is a test.",
                max_tokens=5
            )
        except:
            return False
        else:
            return True

def creds_entered():
    if is_api_key_valid(st.session_state['password']):
        st.session_state['authenticated'] = True
    else:
        st.session_state['authenticated'] = False
        st.error('Invalid API key')

def api_credentials():
    if "authenticated" not in st.session_state:
        st.text_input('Enter OpenAI API key:', key = 'password', on_change = creds_entered)
        st.write("You can find your OpenAI api key [here](https://platform.openai.com/account/api-keys)")
        return False
    else:
        if st.session_state['authenticated']:
            return True
        else:
            st.text_input('Enter OpenAI API key:', key = 'password', on_change = creds_entered)
            st.write("You can find your OpenAI api key [here](https://platform.openai.com/account/api-keys)")
            return False
