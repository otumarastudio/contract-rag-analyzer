from config import PINECONE_API_KEY, OPENAI_API_KEY
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


class QueryProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", dimensions=3072, openai_api_key=OPENAI_API_KEY)
        self.model = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY)

    async def basic_query(self, project_id: str, query: str) -> str:
        namespace = project_id
        vectorstore = PineconeVectorStore(
            index_name="ragcontract", embedding=self.embeddings, namespace=namespace)
        results = await vectorstore.asimilarity_search(query)
        context = "\n".join([result.page_content for result in results])

        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        chain = prompt | self.model | output_parser
        response = await chain.ainvoke({"context": context, "question": query})
        return response

    async def query_with_enhancement(self, project_id: str, query: str) -> str:
        enhancement_prompt = ChatPromptTemplate.from_template(
            "Improve the following query for better search results: {query}")
        enhanced_query = await self.model.ainvoke(enhancement_prompt.invoke({"query": query}))

        return await self.basic_query(project_id, enhanced_query.content)

    async def query_with_split(self, project_id: str, query: str) -> str:
        split_prompt = ChatPromptTemplate.from_template(
            "Split the following complex query into simpler sub-queries: {query}")
        split_queries = await self.model.ainvoke(split_prompt.invoke({"query": query}))
        sub_queries = split_queries.content.split("\n")

        namespace = project_id
        vectorstore = PineconeVectorStore(
            index_name="ragcontract", embedding=self.embeddings, namespace=namespace)

        combined_results = []
        for sub_query in sub_queries:
            results = await vectorstore.asimilarity_search(sub_query)
            combined_results.extend(results)

        context = "\n".join(
            [result.page_content for result in combined_results])

        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        chain = prompt | self.model | output_parser
        response = await chain.ainvoke({"context": context, "question": query})
        return response
