# core/data_ingestion.py
from langchain_community.document_loaders import PyMuPDFLoader

def load_document(file_path):
    loader = PyMuPDFLoader(file_path)
    return loader.load()
