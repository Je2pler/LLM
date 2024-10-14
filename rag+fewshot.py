import streamlit as st
import google.generativeai as genai
import chromadb.utils.embedding_functions.google_embedding_function
import chromadb
from typing import Callable, List, Dict, Tuple, Generator
import os
import pandas as pd
import path_to_training

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
        
        self.chat = self.model.start_chat(history=ChatBot.load_few_shot_history() + [
            {
                'role': 'model' if  message['role']=='ai' else message['role'],
                'parts': message['message']
            }
            for message in history
        ] )

        self.db = db
    
    def load_few_shot_history():
        examples = list()

        for path, name in zip(path_to_training.list_of_exams_path, path_to_training.list_of_exams_name):
            print(f'Loading exam {name}')
            examples += ChatBot.load_training_data(path, name)
        
        return examples
    
    @st.cache_data
    def load_training_data(path: str, name: str) -> List[Dict[str, str]]:
        exam = os.path.join(path, name)
        qa_pairs = list()
        files = dict()

        data = pd.read_csv(exam, quotechar='"', delimiter=';', escapechar='\\')

        for index, row in data.iterrows():
            question = row['question']
            answer = row['answer']
            if row['extra_material']!= "Null":
                file_path = os.path.join(path, row['extra_material'])
                if file_path not in files:
                    print(f'Attemping to upload {file_path}')
                    files[file_path] = genai.upload_file(file_path)
                else:
                    print(f'Found cache for {file_path}')
                question = [question, files[file_path]]
            if '.py' in answer:
                with open(exam, encoding='utf-8') as file:
                    code = ''.join(file.readlines())
                    answer = code
            elif '.png' in answer:
                continue
            qa_pairs.append({'role': 'user', 'parts': question})
            qa_pairs.append({'role': 'model', 'parts': answer})

        return qa_pairs
    
    def check_relevance(self, question: str, answer: str, context: str) -> bool:
        response = self.model.generate_content(
            f'<instruction>Was the following context used to answer the question? '+
            f'Answer yes or no. </instruction><context>{context}</context>'+
            f'<question>{question}</question>' +
            f'<answer>{answer}</answer>'
        )
        return 'yes' in response.text.lower()
    
    def __call__(self, question: str, prompt: str, contexts: List[str], on_complete: Callable[[str], None] = lambda x: None) -> Generator[str, None, None]:
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
            if self.check_relevance(question, answer, context)
        ]

        if len(refrences) > 0:
            ref = f'\n**Refrences**: Barber,  David., *Bayesian Reasoning and Machine Learning*, ' + ', '.join(refrences)
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
Answer the question and explain it to someone who is unfamiliar with the course. If possible, answer using the course book as context. Otherwise, inform the user that you are not answering using the course book.\n
</instruction>\n\n

<course book>\n
{context}\n
</course book>\n\n

<question>\n
{question}\n
</question>
    """, db_result

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

@st.cache_data
def upload_to_gemini(file_path, *args, **kwargs):
    return genai.upload_file(file_path, *args, **kwargs)

def draw_page(chat_bot: ChatBot) -> None:
    """
    Produces streamlit page. 

    ## Parameters
     - ``chat_bot`` Chatbot. 
    """

    # Write title
    st.header('APML AI Tutor')

    st.sidebar.title('Upload file')
    uploaded_file = st.sidebar.file_uploader("Upload a file", label_visibility="collapsed")
    st.sidebar.title("Settings")
    developer_mode = st.sidebar.toggle('Developer Mode')

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            if developer_mode and message['role'] == 'user':
                st.markdown(message['prompt'])
            else:
                st.markdown(message['message'])
            
            if 'image_path' in message:
                st.image(message['image_path'], width=200)

    # Accept user input
    if user_input := st.chat_input('Say something...'):

        prompt, refrences = chat_bot.generate_prompt_and_references(user_input)
        
        st.session_state.messages.append({
            'role': 'user',
            'message': user_input,
            'prompt': prompt
        })

        with st.chat_message('user'):
            if developer_mode:
                st.markdown(prompt)
            else:
                st.markdown(user_input)

            # Handle the uploaded file
            if uploaded_file is not None:
                print(uploaded_file.name)
                print(uploaded_file._file_urls.upload_url)
                file_path = save_uploaded_file(uploaded_file)
                myfile = upload_to_gemini(file_path)
                prompt = [prompt, myfile]
                st.session_state.messages[-1]['image_path'] = file_path
                st.image(file_path, width=200)

        # Write response
        response = chat_bot(
            user_input,
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
    st.set_page_config('APML AI Tutor')

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