# core/embedding.py
from langchain_openai import OpenAIEmbeddings

def create_embeddings():
    return OpenAIEmbeddings()