import chromadb.utils.embedding_functions.google_embedding_function
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
import chromadb
import os

print('Configuring')

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
embedding_function = chromadb.utils.embedding_functions.google_embedding_function.GoogleGenerativeAiEmbeddingFunction(api_key=os.getenv('GOOGLE_API_KEY'))

NAME = 'APML-book'

semantic_splitter = SemanticChunker(
    GoogleGenerativeAIEmbeddings(model="models/embedding-001"), 
    number_of_chunks=500
)

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

db = chromadb.PersistentClient('./.db')

print('Initializing database')

if NAME in (collection.name for collection in db.list_collections()):
    collection = db.get_collection(NAME, embedding_function=embedding_function)
else:
    collection = db.create_collection(NAME, embedding_function=embedding_function)

print('Reading data')

with open('training_data/output.tex', encoding='utf-8') as file:
    text = '\n'.join(file.readlines())

print('Chunking data')

preliminary_chunks = semantic_splitter.split_text(text)
chunks = list()
I = len(preliminary_chunks)

for i, chunk in enumerate(preliminary_chunks):
    print(f'Checking {i}/{I}', end='\r')
    if len(chunk) > 10_000:
        chunks += recursive_splitter.split_text(chunk)
    else:
        chunks.append(chunk)

print(f'Checking {I}/{I}')

I = len(chunks)

for i, chunk in enumerate(chunks):
    print(f'Embedding {i}/{I}', end='\r')
    collection.upsert(
        documents=[chunk],
        ids=[f'id{i}']
    )

print(f'Embedding: {I}/{I}')

results = collection.query(query_texts=['What is the differance between supervised and unsupervised learning? '], n_results=10)
print('\n\n----------\n\n'.join(results['documents'][0]))
