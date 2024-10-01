import streamlit as st
import google.generativeai as genai
import chromadb.utils.embedding_functions.google_embedding_function
import chromadb
from typing import Callable, List, Dict
import os

class VectorDatabase:
    GEMENI_EMBEDDING = chromadb.utils.embedding_functions.google_embedding_function.GoogleGenerativeAiEmbeddingFunction(api_key=st.secrets.gemini.api_key)

    def __init__(self, collection_name: str,  embedding_function = GEMENI_EMBEDDING):
        self.db = chromadb.PersistentClient('./.db')

        if collection_name in (collection.name for collection in self.db.list_collections()):
            self.collection = self.db.get_collection(collection_name, embedding_function=embedding_function)
        else:
            raise ValueError(f'Could not find chroma db collection "{collection_name}"')
    
    def query(self, query_str: str) -> List[str]:
        return self.collection.query(query_texts=[query_str])['documents']

class ChatBot:
    def __init__(self, history: List[Dict[str, str]], db: VectorDatabase):
        self.model = genai.GenerativeModel(
            model_name = 'gemini-1.5-flash',
            system_instruction="You are an expert in the machine learning course: advanced probabilistic machine learning. If you are unsure about an answer, say so."
        )
        
        self.chat = self.model.start_chat(history=[
            {
                'role': 'model' if  message['role']=='ai' else message['role'],
                'parts': message['message']
            }
            for message in history
        ])

        self.db = db
    
    def __call__(self, prompt: str) -> str:
        """
        Generate response to prompt. 

        ## Parameters
         - ``prompt`` Prompt for model. 
        """
        return self.chat.send_message(prompt).text

    def generate_prompt(self, question: str) -> str:
        context = '\n\n'.join(self.db.query(question))

        return f"""
<instruction>
Use the context to answer the question. If the answer doesn't exist within the context, say that you don't know the answer. 
</instruction>\n\n

<context>
{context}
</context>\n\n

<question>
{question}
</question>
    """

def gemini_response_generator(model: genai.GenerativeModel, prompt: str) -> str:
    """
    Produces a response for the ``prompt``
    through the Google Gemeni API. 

    ## Parameters
     - ``model`` The ``genai.GenerativeModel`` to use. 
     - ``prompt`` Prompt to submit to Gemini. 
    """
    return model.generate_content(prompt).text

def draw_page(chat_bot: ChatBot) -> None:
    """
    Produces streamlit page. 

    ## Parameters
     - ``response_generator`` Callback function to generate response. 
    """
    # Write title
    st.header('1RT730 Chatbot')

    st.sidebar.title("Predefinied functions")
    developer_mode = st.sidebar.toggle('Developer Mode')
    st.sidebar.button('Generate Exam', generate_exam)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            if developer_mode and message['role'] == 'user':
                st.markdown(message['prompt'])
            else:
                st.markdown(message['message'])

    # Accept user input
    if user_input := st.chat_input('Say something...'):
        prompt = chat_bot.generate_prompt(user_input)
        print('**************')
        print(prompt)
        print('**************')

        with st.chat_message('user'):
            if developer_mode:
                st.markdown(prompt)
            else:
                st.markdown(user_input)
        
        st.session_state.messages.append({
            'role': 'user',
            'message': user_input,
            'prompt': prompt
        })

        # Write response
        response = chat_bot(prompt)

        with st.chat_message('ai'):
            st.write_stream(list(response))
        
        st.session_state.messages.append({
            'role': 'ai',
            'message': response
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
            'message': "Welcome to the 1RT730 Chatbot. How can I help you today?"
        }]
    
    # Load db
    db = VectorDatabase('APML-book')

    # Create chatbot
    chat_bot = ChatBot(st.session_state.messages, db)

    # Draw page
    draw_page(chat_bot)

if __name__ == '__main__': 
    genai.configure(api_key=st.secrets.gemini.api_key)
    main()