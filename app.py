import os
import sys 

# 현재 파일의 디렉토리를 파이썬 경로에 추가
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, current_dir)
sys.path.append(os.path.join(os.path.dirname(__file__), 'rag'))


from flask import Flask, render_template, request, redirect, url_for, jsonify, g
import markdown2
import re
from qa_data import qa_pairs
from rag.main import RAGSystem
from rag.utils.logger import logger
import json

app = Flask(__name__)


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
    if request.method == 'POST':
        return naive_rag()
    return redirect(url_for('naive_rag'))

@app.route('/naive_rag', methods=['GET', 'POST'])
def naive_rag():
    if request.method == 'POST':
        question = request.form['question']
        answer = qa_pairs.get(question, "죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다.")
        answer_html = markdown2.markdown(answer, extras=["fenced-code-blocks"])
        answer_html = add_language_class(answer_html)
        return render_template('naive_rag.html', question=question, answer=answer_html, qa_pairs=qa_pairs)
    return render_template('naive_rag.html', qa_pairs=qa_pairs)

@app.route('/advanced_rag', methods=['GET', 'POST'])
def advanced_rag():
    if request.method == 'POST':
        question = request.form['question']
        try:
            rag_system = get_rag_system()
            
            logger.info(f"Processing query: {question}")
            result = rag_system.process_query(question)
            logger.info("Query processed successfully")
            
            answer_html = markdown2.markdown(result["answer"], extras=["fenced-code-blocks"])
            answer_html = add_language_class(answer_html)
            
            search_results_html = ""
            for i, doc in enumerate(result["search_results"], 1):
                search_results_html += f"<h4>문서 조각 {i}</h4>"
                search_results_html += f"<p>{doc.page_content}</p>"
                search_results_html += f"<p><strong>메타데이터:</strong> {json.dumps(doc.metadata, ensure_ascii=False)}</p>"
            
            return render_template('advanced_rag.html', question=question, answer=answer_html, search_results=search_results_html)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return render_template('advanced_rag.html')

@app.route('/prompt_setting')
def prompt_setting():
    return render_template('prompt_setting.html')

@app.teardown_appcontext
def teardown_rag_system(exception):
    rag_system = g.pop('rag_system', None)
    if rag_system is not None:
        # 필요한 경우 여기에 RAG 시스템의 정리 로직을 추가할 수 있습니다.
        logger.info("RAG System cleaned up.")

if __name__ == '__main__':
    app.run(debug=True)
