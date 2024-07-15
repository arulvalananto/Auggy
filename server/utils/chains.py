from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.llm_models import LanguageModels
from utils.prompt_templates import PromptTemplatesGenerator


class Chain:
    @staticmethod
    def format_user_query(query: str) -> str:
        # format question prompt
        prompt = ChatPromptTemplate.from_template(
            PromptTemplatesGenerator.improve_query()
        )

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | StrOutputParser()

        # invoke
        formatted_user_query = chain.invoke({"query": query})

        return formatted_user_query

    @staticmethod
    def classify_query(query: str) -> str:
        # format question prompt
        prompt = ChatPromptTemplate.from_template(
            PromptTemplatesGenerator.classify_query()
        )

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | StrOutputParser()

        apps = [
            "paddyfield",
            "gretyHR",
            "google calendar",
            "slack",
            "google meet",
            "gmail",
        ]

        tasks = ["image generation", "text generation", "code generation"]

        # invoke
        classification = chain.invoke({"query": query, "apps": apps, "tasks": tasks})

        return classification
