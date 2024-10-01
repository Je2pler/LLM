import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

from typing import Callable, List, Dict

class ChatBot:
    def __init__(self, history: List[Dict[str, str]]):
        self.model = genai.GenerativeModel(
            model_name = 'gemini-1.5-flash',
            #system_instruction="You are an expert in the machine learning course: advanced probabilistic machine learning. If you are unsure about an answer, say so."
            )
        self.chat = self.model.start_chat(history=[
            {
                'role': 'model' if  message['role']=='ai' else message['role'],
                'parts': message['content']
            }
            for message in history
        ])
    
    def __call__(self, prompt: list) -> str:
        """
        Generate response to prompt. 

        ## Parameters
         - ``prompt`` Prompt for model. 
        """
        return self.chat.send_message(prompt).text
    
def save_uploaded_file(uploaded_file):
    # Create a temporary path to save the file
    temp_file_path = os.path.join("temp", uploaded_file.name)
    
    # Ensure the temp directory exists
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # Save the file to disk
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return temp_file_path

def draw_page(response_generator: Callable[[str], str]) -> None:
    """
    Produces Streamlit page. 

    ## Parameters
     - ``response_generator`` Callback function to generate response. 
    """
    # Write title
    st.header('1RT730 Chatbot')

    st.sidebar.title("Predefined functions")
    st.sidebar.button('Generate Exam', generate_exam)
    uploaded_file = st.sidebar.file_uploader("Upload a file", label_visibility="collapsed")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # Accept user input
    prompt = st.chat_input('Say something...')
    
    if prompt:
        with st.chat_message('user'):
            st.markdown(prompt)
        
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt
        })

        prompt = [prompt]

        # Handle the uploaded file
        if uploaded_file is not None:
            print(uploaded_file.name)
            print(uploaded_file._file_urls.upload_url)
            file_path = save_uploaded_file(uploaded_file)
            myfile = genai.upload_file(file_path)
            prompt.append(myfile)
        response = response_generator(prompt)

        with st.chat_message('ai'):
            st.write(response)
        
        st.session_state.messages.append({
            'role': 'ai',
            'content': response
        })

def generate_exam(): 
    pass

def main() -> None:
    """
    Main function. 
    """
    # Initilize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [{
            'role': 'ai',
            'content': "Welcome to the 1RT730 Chatbot. How can I help you today?"
        }]
    
    # Create chatbot
    chat_bot = ChatBot(st.session_state.messages)

    # Draw page
    draw_page(chat_bot)

if __name__ == '__main__': 
    genai.configure(api_key=st.secrets.gemini.api_key)
    main()