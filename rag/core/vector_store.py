# core/vector_store.py
# from langchain_community.vectorstores import Chroma

# SQLite 버전 오버라이드 우분투 트러블슛 시 추가 함.
from langchain_chroma import Chroma


def create_vectorstore(documents, embeddings, persist_directory):
    return Chroma.from_documents(documents, embeddings, persist_directory=persist_directory)


def load_vectorstore(persist_directory, embeddings):
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
