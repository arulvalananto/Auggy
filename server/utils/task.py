import os

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from utils.prompt_templates import PromptTemplatesGenerator
from utils.llm_models import LanguageModels
from langchain.prompts import ChatPromptTemplate


class Task:
    @staticmethod
    def generate_response(question: str) -> str:
        # prompt
        # https://smith.langchain.com/hub/shreyshah/llm_agent
        prompt = ChatPromptTemplate.from_template(
            template=PromptTemplatesGenerator.task(),
        )

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | StrOutputParser()

        return chain.invoke({"query": question})
