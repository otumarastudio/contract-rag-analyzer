import json
from rag.utils.logger import logger
from rag.utils.config import *
from rag.main import RAGSystem
from qa_data import qa_pairs
import re
import markdown2
from flask import Flask, render_template, request, redirect, url_for, jsonify, g, session
# import pyrebase
# import firebase_admin
# from firebase_admin import credentials, auth
# from rag.utils.config import FIREBASE_WEB_API_KEY
# from rag.utils.config import (
#     FIREBASE_WEB_API_KEY,
#     FIREBASE_AUTH_DOMAIN,
#     FIREBASE_PROJECT_ID,
#     FIREBASE_STORAGE_BUCKET,
#     FIREBASE_MESSAGING_SENDER_ID,
#     FIREBASE_APP_ID,
#     FIREBASE_PRIVATE_KEY_ID,
#     FIREBASE_PRIVATE_KEY,
#     FIREBASE_CLIENT_EMAIL,
#     FIREBASE_CLIENT_ID,
#     FIREBASE_CLIENT_CERT_URL,
#     FLASK_SECRET_KEY
# )

import sys
import os

# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# 현재 파일의 디렉토리를 파이썬 경로에 추가
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, current_dir)
sys.path.append(os.path.join(os.path.dirname(__file__), 'rag'))


app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect(url_for('index'))
        except:
            return 'Failed to login'
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


def get_rag_system():
    if 'rag_system' not in g:
        try:
            g.rag_system = RAGSystem()
            logger.info("RAG System initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize RAG System: {str(e)}")
            raise
    return g.rag_system


@app.before_request
def before_request():
    try:
        get_rag_system()
    except Exception as e:
        logger.error(f"Error initializing RAG System: {str(e)}")


def add_language_class(html):
    return re.sub(r'<pre><code>', r'<pre><code class="language-python">', html)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('advanced_rag'))


# @app.route('/naive_rag', methods=['GET', 'POST'])
# def naive_rag():
#     if request.method == 'POST':
#         question = request.form['question']
#         answer = qa_pairs.get(question, "죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다.")
#         answer_html = markdown2.markdown(answer, extras=["fenced-code-blocks"])
#         answer_html = add_language_class(answer_html)
#         return render_template('naive_rag.html', question=question, answer=answer_html, qa_pairs=qa_pairs)
#     return render_template('naive_rag.html', qa_pairs=qa_pairs)

# def format_metadata(metadata):
#     relevant_fields = ["page", "total_pages", "source", "subject", "title"]
#     formatted_metadata = {k: v for k, v in metadata.items() if k in relevant_fields}
#     return json.dumps(formatted_metadata, ensure_ascii=False)

def format_metadata(metadata):
    relevant_fields = ["page", "total_pages", "source"]
    formatted_metadata = {k: v for k,
                          v in metadata.items() if k in relevant_fields}
    return " | ".join(f"{k}: {v}" for k, v in formatted_metadata.items())


@app.route('/advanced_rag', methods=['GET', 'POST'])
def advanced_rag():
    if request.method == 'POST':
        question = request.form['question']
        try:
            rag_system = get_rag_system()

            logger.info(f"Processing query: {question}")
            # enhanced_query = rag_system.query_enhancing(question)  # query_enhancing 실행
            result = rag_system.process_query(question)  # original query 사용
            logger.info("Query processed successfully")

            answer_html = markdown2.markdown(
                result["answer"], extras=["fenced-code-blocks"])
            answer_html = add_language_class(answer_html)

            search_results_html = ""
            for i, doc in enumerate(result["search_results"], 1):
                search_results_html += f"<div class='list-group-item'>"
                search_results_html += f"<p class='mb-1'>{doc.page_content}</p>"
                search_results_html += f"<small class='text-muted'>정보: {format_metadata(doc.metadata)}</small>"
                search_results_html += "</div>"
                if i < len(result["search_results"]):
                    search_results_html += "<hr>"

            # enhanced_query 추가
            enhanced_query = result.get("enhanced_query", "")

            return render_template('advanced_rag.html', question=question, enhanced_query=enhanced_query, answer=answer_html, search_results=search_results_html)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return render_template('advanced_rag.html')


@app.route('/documents')
def documents_manage():
    return render_template('documents.html')


@app.teardown_appcontext
def teardown_rag_system(exception):
    rag_system = g.pop('rag_system', None)
    if rag_system is not None:
        # 필요한 경우 여기에 RAG 시스템의 정리 로직을 추가할 수 있습니다.
        logger.info("RAG System cleaned up.")


if __name__ == '__main__':
    app.run(debug=True)
