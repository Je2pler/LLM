from pypdf import PdfReader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import chromadb
import toml
import os

with open('.streamlit/secrets.toml', 'r') as file:
    secrets = toml.load(file)

os.environ["GOOGLE_API_KEY"] = secrets['gemini']['api_key']
genai.configure(api_key=secrets['gemini']['api_key'])

NAME = 'APML-book'

class GemeniEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input_doc: chromadb.Documents) -> chromadb.Embeddings:
        return genai.embed_content(
            model = 'models/embedding-001',
            task_type = 'retrieval_document',
            content = input_doc
        )['embedding']

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
text_splitter = SemanticChunker(embeddings)

db = chromadb.PersistentClient('./.db')

if NAME in (collection.name for collection in db.list_collections()):
    collection = db.get_collection(NAME, embedding_function=GemeniEmbeddingFunction())
else:
    collection = db.create_collection(NAME, embedding_function=GemeniEmbeddingFunction())

reader = PdfReader(f'{NAME}.pdf')

text = '\n'.join([
    '\n'.join(page.extract_text().split('\n')[1:-3])
    for page in reader.pages[25:661]
])

chunks = text_splitter.split_text(text)

collection.upsert(
    documents=chunks,
    # metadatas=[
    #     document.metadata['page']
    #     for document in documents
    # ],
    ids=[
        f'id{x}'
        for x in range(len(chunks))
    ]
)

print(f'Chunks: {chunks[:50]}')

results = collection.query(query_texts='Explain random forest', n_results=10)
print('\n\n----------\n\n'.join(results['documents'][0]))
