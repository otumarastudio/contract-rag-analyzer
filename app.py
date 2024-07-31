from flask import Flask, render_template, request, redirect, url_for
import markdown2
import re
from qa_data import qa_pairs

app = Flask(__name__)

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

@app.route('/advanced_rag')
def advanced_rag():
    return render_template('advanced_rag.html')

@app.route('/prompt_setting')
def prompt_setting():
    return render_template('prompt_setting.html')

if __name__ == '__main__':
    app.run(debug=True)