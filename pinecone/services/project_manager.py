import os
from fastapi import HTTPException, UploadFile
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from config import PINECONE_API_KEY
from langchain_openai import OpenAIEmbeddings


class ProjectManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", dimensions=3072)

    async def upload_project(self, project_name: str, file: UploadFile) -> str:
        # 파일 저장
        file_path = f"./uploaded_documents/{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(
                status_code=500, details=f"Error saving file: {str(e)}")

        # 문서 로드 및 분할
        try:
            loader = TextLoader(file_path)
            documents = loader.load()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error loading file: {str(e)}")

        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = splitter.split_documents(documents)
        docs_with_metadata = self.add_metadata(docs, project_name)

        # 벡터 DB에 업로드
        namespace = project_name

        try:
            vectorstore = PineconeVectorStore(
                index_name="ragcontract", embedding=self.embeddings, namespace=namespace)
            await vectorstore.from_documents(docs_with_metadata)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error uploading to vector store: {str(e)}")
        return "Upload successful"

    def add_metadata(self, documents, project_name: str):
        for doc in documents:
            doc.metadata['project'] = project_name
        return documents
