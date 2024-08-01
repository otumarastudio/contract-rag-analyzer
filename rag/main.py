# main.py
import os
import sys
import logging

# 현재 파일의 디렉토리를 파이썬 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from flask import Flask, request, render_template, jsonify, g
import markdown2
import re
from utils.config import CHROMADB_PATH, OPENAI_API_KEY
from utils.logger import log_function, logger
from core.data_ingestion import load_document
from core.data_processing import split_documents
from core.embedding import create_embeddings
from core.vector_store import create_vectorstore, load_vectorstore
from core.retrieval import create_retriever
from core.query_processing import create_prompt_template, query_enhancing  # 수정된 부분
from core.answer_generation import create_llm, create_chain

logging.basicConfig(level=logging.INFO)

class RAGSystem:
    @log_function
    def __init__(self):
        try:
            logging.info(f"CHROMADB_PATH: {CHROMADB_PATH}")
            self.embeddings = create_embeddings()
            self.db = load_vectorstore(CHROMADB_PATH, self.embeddings)
            self.retriever = create_retriever(self.db, search_type="mmr", k=5)
            self.prompt = create_prompt_template()
            self.llm = create_llm()
            self.chain = create_chain(self.retriever, self.prompt, self.llm)
        except Exception as e:
            logger.error(f"Error initializing RAG System: {str(e)}")
            raise


    @log_function
    def query_enhancing(self, question):
        try:
            enhanced_query = query_enhancing(question)
            logger.info(f"Enhanced Query: {enhanced_query}")
            return enhanced_query
        except Exception as e:
            logger.error(f"Error enhancing query: {str(e)}")
            raise

    @log_function
    def process_query(self, question):
        try:
            logger.info(f"Original query: {question}")
            enhanced_query = self.query_enhancing(question)  # query_enhancing 함수 호출
            logger.info(f"Enhanced query: {enhanced_query}")

            search_results = self.retriever.invoke(enhanced_query)
            logger.info(f"Retrieved {len(search_results)} documents")
            for i, doc in enumerate(search_results, 1):
                logger.info(f"Document {i}: {doc.page_content[:100]}...")  # Log first 100 characters of each document
            
            answer = self.chain.invoke(enhanced_query)
            logger.info(f"Generated answer: {answer[:100]}...")  # Log first 100 characters of the answer
            
            return {
                "answer": answer,
                "search_results": search_results,
                "enhanced_query": enhanced_query  # 수정된 부분
            }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise

    @log_function
    def ingest_and_process(self, file_path):
        try:
            documents = load_document(file_path)
            split_docs = split_documents(documents)
            self.db = create_vectorstore(split_docs, self.embeddings, CHROMADB_PATH)
            self.retriever = create_retriever(self.db, search_type="similarity", k=7)
            self.chain = create_chain(self.retriever, self.prompt, self.llm)
            logger.info(f"Document ingested and processed: {file_path}")
        except Exception as e:
            logger.error(f"Error ingesting and processing document: {str(e)}")
            raise

# CLI 모드를 위한 함수
def run_cli():
    rag_system = RAGSystem()
    logger.info("RAG System ready for queries.")
    while True:
        question = input("질문을 입력하세요 (종료하려면 'exit' 입력): ")
        if question.lower() == 'exit':
            logger.info("Exiting RAG System.")
            break
        logger.info(f"Processing query: {question}")
        result = rag_system.process_query(question)
        
        print("\n답변:")
        print(result["answer"])
        
        print("\n검색된 문서 조각들:")
        for i, doc in enumerate(result["search_results"], 1):
            print(f"\n--- 문서 조각 {i} ---")
            print(doc.page_content)
            print(f"메타데이터: {doc.metadata}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    run_cli()
