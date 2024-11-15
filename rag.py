import streamlit as st
import google.generativeai as genai
import chromadb.utils.embedding_functions.google_embedding_function
import chromadb
from typing import Callable, List, Dict, Tuple, Generator
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
        return list(zip(
            [
                int(id.split(':')[0])-24
                for id in 
                self.collection.query(query_texts=[query_str], n_results=4)['ids'][0]
            ],
            self.collection.query(query_texts=[query_str], n_results=4)['documents'][0]
        ))

class ChatBot:
    def __init__(self, history: List[Dict[str, str]], db: VectorDatabase):
        self.model = genai.GenerativeModel(
            model_name = 'gemini-1.5-flash',
            system_instruction="You are an expert in the machine learning course: advanced probabilistic machine learning. If you are unsure about an answer, say so.",
            generation_config={
                'temperature': 0
            }
        )
        
        self.chat = self.model.start_chat(history=[
            {
                'role': 'model' if  message['role']=='ai' else message['role'],
                'parts': message['message']
            }
            for message in history
        ] )

        self.db = db
    
    def check_relevance(self, answer: str, context: str) -> bool:
        response = self.model.generate_content(
            f'<instruction>Was the following context used to create the following answer? '+
            f'Answer yes or no. </instruction><context>{context}</context>'+
            f'<answer>{answer}</answer>'
        )
        return 'yes' in response.text.lower()
    
    def __call__(self, prompt: str, contexts: List[str], on_complete: Callable[[str], None] = lambda x: None) -> Generator[str, None, None]:
        """
        Generate response to prompt. 

        ## Parameters
         - ``prompt`` Prompt for model. 
        """
        answer = ''

        for chunk in self.chat.send_message(prompt, stream=True):
            yield chunk.text
            answer += chunk.text

        refrences = [
            f'p{page_nr}'
            for page_nr, context in contexts
            if self.check_relevance(answer, context)
        ]

        if len(refrences) > 0:
            ref = f'\n**Refrences**: ' + ', '.join(refrences)
            answer += ref
            yield ref
        
        on_complete(answer)

    def generate_prompt_and_references(self, question: str) -> Tuple[str, Tuple[int, str]]:
        db_result = self.db.query(question)

        context = '\n\n'.join([
            f'<course_book>\nPage number: {page_nr}\n\n{segment}\n</course_book>'
            for page_nr, segment in db_result
        ])

        return f"""
<instruction>\n
Answer the question and explain it to someone who is unfamilliar with the course. If possible, answer using the course book as context. Otherwise, inform the user that you are not answering using the course book.\n
</instruction>\n\n

<course book>\n
{context}\n
</course book>\n\n

<question>\n
{question}\n
</question>
    """, db_result

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
    # Page config
    st.set_page_config('APML AI Tutor')

    # Write title
    st.header('APML AI Tutor')

    st.sidebar.title("Settings")
    developer_mode = st.sidebar.toggle('Developer Mode')

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            if developer_mode and message['role'] == 'user':
                st.markdown(message['prompt'])
            else:
                st.markdown(message['message'])

    # Accept user input
    if user_input := st.chat_input('Say something...'):
        prompt, refrences = chat_bot.generate_prompt_and_references(user_input)

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
        response = chat_bot(
            prompt, 
            refrences, 
            lambda response: st.session_state.messages.append({
                'role': 'ai',
                'message': response
            })
        )

        with st.chat_message('ai'):
            st.write_stream(response)

def main() -> None:
    """
    Main function. 
    """
    # Initilize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [{
            'role': 'ai',
            'message': "What can I teach you today? "
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