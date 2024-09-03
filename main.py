import streamlit as st
import google.generativeai as genai

from typing import Callable

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

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = list()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input('Say something...'):
        with st.chat_message('user'):
            st.markdown(prompt)
        
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt
        })

        # Write response
        response = response_generator(prompt)

        with st.chat_message('assistant'):
            st.markdown(response)
        
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response
        })

def main() -> None:
    """
    Main function. 
    """
    genai.configure(st.secrets.gemini.api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    draw_page(lambda prompt: gemini_response_generator(model, prompt))

if __name__ == '__main__': 
    main()
