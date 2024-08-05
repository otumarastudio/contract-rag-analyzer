
# core/query_processing.py
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def create_prompt_template():
    return PromptTemplate.from_template(
        """당신은 건설 프로젝트의 계약자를 위한 계약서 분석 전문가입니다. 주어진 질문에 대해 계약서의 관련 부분을 분석하고 핵심적인 답변을 제공해야 합니다. 다음 지침을 따라 답변을 작성하세요:
        1. 질문의 의도를 정확히 파악하여 답변하세요.
        2. 답변은 bullet point 형식으로 핵심 내용만 간결하게 작성하세요. 합니다 가 아닌 함. 이런식의 개조체 보고체로 작성하세요.
        3. 제공된 계약서 조각들에서 질문에 대한 명확한 답변을 찾을 수 없다면, 어떤 부분에 대한 답변이 없는지 명시하세요.
        4. 질문의 일부나 전체에 대한 답을 모르거나 관련 정보가 없다면, 어떤 질문에 대한 답변을 찾을 수 없는지 정확히 명기해주세요.
        5. 추측하거나 계약서에 명시되지 않은 정보를 절대 제공하지 마십시오.
        6. 답변은 항상 객관적이고 사실에 기반해야 하며, 계약자의 입장에서 중요한 정보를 강조하세요.
        7. 답변은 마크다운으로 작성하세요.
        8. 가장 상단에 질문에 대한 답변의 핵심요약을 제공하세요.
        #질문: {question}
        #계약서 관련 부분: {context}
        #답변:"""
    )


def query_enhancing(question):
    # GPT 모델을 통해 사용자 쿼리를 수정하는 함수
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)  # GPT 모델 초기화
    prompt = ChatPromptTemplate.from_messages([
(
"system", """You are an AI assistant specializing in construction contract analysis for large industrial projects (e.g., oil & gas, power plants). Your task is to transform user queries into enhanced search queries for cosine similarity matching in a vector database of contract clauses.

Given a user's query:
1. Analyze the intent and key concepts.
2. Identify relevant contract terminology and project management aspects.
3. Expand the query with related terms, synonyms, and industry-specific language.
4. Formulate a clear, concise, and targeted English query that will maximize the chances of finding relevant contract clauses.

Respond only with the enhanced query, without explanations or additional text.

Example:
User: "What are the contractor's responsibilities for project management?"
Enhanced query: "contractor obligations project management control work supervision reporting progress scheduling quality HSE interfaces subcontractor coordination""",
), ("human", """질문: {question} 
최적화된 쿼리:"""),])
    chain = prompt | llm
    response = chain.invoke(   
    {"question": question,   
    })   
    # 응답의 텍스트 부분을 추출
    #response = llm.invoke(messages)

    return response.content