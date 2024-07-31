from dotenv import load_dotenv
import os

load_dotenv()

LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# CHROMADB_PATH = os.path.abspath(os.getenv("CHROMADB_PATH", "./chroma_db"))
CHROMADB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chroma_db'))

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 50
MODEL_NAME = "gpt-4o"
TEMPERATURE = 0
