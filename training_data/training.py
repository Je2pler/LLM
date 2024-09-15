from pypdf import PdfReader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import chromadb
import os

os.environ["GOOGLE_API_KEY"] = 'AIzaSyCWlzRrc0mFqXqv88n3vutOiWLkgFa08cE'
genai.configure(api_key='AIzaSyCWlzRrc0mFqXqv88n3vutOiWLkgFa08cE')

NAME = 'sml-book'

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

text_list = [page.extract_text() for page in reader.pages[70:100]]
text_list = [text for text in text_list if len(text) > 0]

documents = text_splitter.create_documents(
    text_list,
    # [{'page': i+9} for i in range(len(reader.pages[8:]))],
)

collection.upsert(
    documents=[
        document.page_content
        for document in documents
    ],
    # metadatas=[
    #     document.metadata['page']
    #     for document in documents
    # ],
    ids=[
        f'id{x+70}'
        for x in range(len(documents))
    ]
)

results = collection.query(query_texts='Random forest explaination', n_results=10)
print('\n\n----------\n\n'.join(results['documents'][0]))
