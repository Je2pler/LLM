import chromadb.utils.embedding_functions.google_embedding_function
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
import chromadb
import os

def get_paragraphs(path: str):
    for filename in os.listdir(path):
        if filename[-4:] != '.tex':
            continue
    
        page_nr = int(filename[:-4])

        with open(f'{path}/{filename}', encoding='utf-8') as file:
            for paragraph in file.readlines():
                paragraph = paragraph.strip('\n')

                if len(paragraph) > 0:
                    yield page_nr, paragraph

print('Configuring')

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
embedding_function = chromadb.utils.embedding_functions.google_embedding_function.GoogleGenerativeAiEmbeddingFunction(api_key=os.getenv('GOOGLE_API_KEY'))

NAME = 'APML-book'

db = chromadb.PersistentClient('./.db')

print('Initializing database')

if NAME in (collection.name for collection in db.list_collections()):
    collection = db.get_collection(NAME, embedding_function=embedding_function)
else:
    collection = db.create_collection(NAME, embedding_function=embedding_function)

print('Processing data')

paragraphs = list()
page_nrs = list()
cache_length = 0

current_page = 0
paragraphs_on_page = 0

for page_nr, paragraph in get_paragraphs('training_data/APML-book'):
    print(f'Processing page {page_nr}', end='\r')
    page_nrs.append(page_nr)
    paragraphs.append(paragraph)

    if cache_length < 2_500:
        cache_length += len(paragraph)
    else:
        cache_length -= len(paragraphs[0])

        if page_nr != current_page:
            current_page = page_nr
            paragraphs_on_page = 0
        
        collection.upsert(
            documents=['\n\n'.join(paragraphs)],
            embeddings=[
                genai.embed_content(
                    model='models/embedding-001',
                    content=paragraphs[0],
                    task_type='retrieval_document',
                    title='Probobalistic Machine Learning'
                )['embedding']
            ],
            ids=[f'{current_page}:{paragraphs_on_page}']
        )

        page_nrs.pop(0)
        paragraphs.pop(0)

print('\nComplete')