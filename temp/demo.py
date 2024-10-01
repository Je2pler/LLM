import streamlit as st
import google.generativeai as genai

from typing import Callable, List, Dict

class ChatBot:
    def __init__(self, history: List[Dict[str, str]]):
        self.model = genai.GenerativeModel(
            model_name = 'gemini-1.5-flash',
            system_instruction="You are an expert in the machine learning course: advanced probabilistic machine learning. If you are unsure about an answer, say so."
            )
        self.chat = self.model.start_chat(history=[
            {
                'role': 'model' if  message['role']=='ai' else message['role'],
                'parts': message['content']
            }
            for message in history
        ])
    
    def __call__(self, prompt: str) -> str:
        """
        Generate response to prompt. 

        ## Parameters
         - ``prompt`` Prompt for model. 
        """
        return self.chat.send_message(prompt).text

def gemini_response_generator(model: genai.GenerativeModel, prompt: str) -> str:
    """
    Produces a response for the ``prompt``
    through the Google Gemeni API. 

    ## Parameters
     - ``model`` The ``genai.GenerativeModel`` to use. 
     - ``prompt`` Prompt to submit to Gemini. 
    """
    return model.generate_content(prompt).text

def draw_page(response_generator: Callable[[str], str]) -> None:
    """
    Produces streamlit page. 

    ## Parameters
     - ``response_generator`` Callback function to generate response. 
    """
    # Write title
    st.header('1RT730 Chatbot')

    st.sidebar.title("Predefinied functions")
    st.sidebar.button('Generate Exam', generate_exam)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input('Say something...'):
        with st.chat_message('user'):
            instruction = "You are an expert in the machine learning course: advanced probabilistic machine learning. If you are unsure about an answer, say so."
            st.markdown(prompt)
        
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt
        })

        # Write response
        response = response_generator(prompt)

        with st.chat_message('ai'):
            st.write_stream(list(response))
        
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