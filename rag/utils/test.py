from langchain_openai import ChatOpenAI
from config import CHROMADB_PATH, OPENAI_API_KEY
from langchain_core.prompts import ChatPromptTemplate

def query_enhancing(question):
    # GPT 모델을 통해 사용자 쿼리를 수정하는 함수
    model = ChatOpenAI(model="gpt-4o", temperature=0.1)  # GPT 모델 초기화
    prompt = f"""
    사용자가 쿼리를 날리면, 영문의 대형 산업설비(oil&gas, powerplant, etc..) 건설 프로젝트의 계약서의 RAG 시스템의 유사도검색을 위한 query로 변환할 것이다. 사용자의 질문의 의도를 명확히 파악하고, 계약서의 cosine similarity score 검색을 위한 강화된 쿼리를 영문으로 제공하면 된다.
    질문: "{question}"
    최적화된 쿼리: 
    """
    response = model.generate({"messages": [{"role": "user", "content": prompt}]})
    full_response = response.generations[0].text.strip()
    return full_response, response

def query_enhancing2(question):
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
    print(response)
    return response

if __name__ == "__main__":
    question = "Who provides meals and accommodations?"
    response = query_enhancing2(question)
    
    # 전체 응답 출력
    print("Response:")
    print(response.content)
    
