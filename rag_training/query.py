import google.generativeai as genai
import chromadb.utils.embedding_functions.google_embedding_function
import chromadb
from typing import Callable, List, Dict
import os

class VectorDatabase:
    GEMENI_EMBEDDING = chromadb.utils.embedding_functions.google_embedding_function.GoogleGenerativeAiEmbeddingFunction(api_key=os.getenv('GOOGLE_API_KEY'))

    def __init__(self, collection_name: str,  embedding_function = GEMENI_EMBEDDING):
        self.db = chromadb.PersistentClient('./.db')

        if collection_name in (collection.name for collection in self.db.list_collections()):
            self.collection = self.db.get_collection(collection_name, embedding_function=embedding_function)
        else:
            raise ValueError(f'Could not find chroma db collection "{collection_name}"')
    
    def query(self, query_str: str) -> List[str]:
        return list(zip(
            [
                int(id.split(':')[0])
                for id in 
                self.collection.query(query_texts=[query_str], n_results=4)['ids'][0]
            ],
            self.collection.query(query_texts=[query_str], n_results=4)['documents'][0]
        ))

def main():
    db = VectorDatabase('APML-book')

    while True:
        print(db.query(input('> ')))
    

if __name__ == '__main__':
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    main()