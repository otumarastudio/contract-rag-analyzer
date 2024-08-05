# core/vector_store.py
# from langchain_community.vectorstores import Chroma

# SQLite 버전 오버라이드 우분투 트러블슛 시 추가 함.
import pysqlite3 as sqlite3  # pysqlite3를 sqlite3로 임포트
import sys
from langchain_chroma import Chroma

# sys.modules 딕셔너리를 통해 sqlite3 모듈을 pysqlite3 모듈로 오버라이드
sys.modules['sqlite3'] = sqlite3


def create_vectorstore(documents, embeddings, persist_directory):
    return Chroma.from_documents(documents, embeddings, persist_directory=persist_directory)


def load_vectorstore(persist_directory, embeddings):
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
