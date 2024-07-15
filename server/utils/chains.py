from langchain import hub
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from models import Classification
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

        return chain.invoke({"query": query})

    @staticmethod
    def classify_query(query: str) -> str:
        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=Classification)

        prompt = PromptTemplate(
            template=PromptTemplatesGenerator.classify_query(),
            input_variables=["query", "apps", "tasks"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | parser

        apps = [
            "paddyfield",
            "gretyHR",
            "google calendar",
            "slack",
            "google meet",
            "gmail",
        ]

        tasks = ["image generation", "text generation", "code generation"]

        policies = [
            "Remote work policy",
            "Leave policy",
            "Health policy",
            "Reimbursement policy",
        ]

        # invoke
        classification = chain.invoke(
            {"query": query, "apps": apps, "tasks": tasks, "policies": policies}
        )

        return classification

    @staticmethod
    def funny_reply(query: str) -> str:
        # format question prompt
        prompt = hub.pull("sredeemer/joke")

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | StrOutputParser()

        return chain.invoke({"question": query})
