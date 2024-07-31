# core/answer_generation.py
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def create_llm(model_name="gpt-4o", temperature=0.1): # type: ignore
    return ChatOpenAI(model=model_name, temperature=temperature)

ChatOpenAI()

def create_chain(retriever, prompt, llm):
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
            }
        | prompt
        | llm
        | StrOutputParser()
    )
