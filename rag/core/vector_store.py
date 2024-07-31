# core/vector_store.py
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

def create_vectorstore(documents, embeddings, persist_directory):
    return Chroma.from_documents(documents, embeddings, persist_directory=persist_directory)

def load_vectorstore(persist_directory, embeddings):
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
