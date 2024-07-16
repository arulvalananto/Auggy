from langchain import hub
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from models import Classification
from utils.constants import constants
from utils.llm_models import LanguageModels
from utils.prompt_templates import PromptTemplatesGenerator


class Chain:
    def llama3_str_parser():
        llm = LanguageModels.ollama_llama3()

        return llm | StrOutputParser()

    def improve_query(query: str) -> str:
        prompt = hub.pull("promptcyril/fix_spelling_and_grammar")
        chain = prompt | Chain.llama3_str_parser()

        return chain.invoke({"text": query, "accent": "professional"})

    @staticmethod
    def classify_query(query: str) -> Classification:
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

        return chain.invoke(
            {
                "query": query,
                "apps": constants["apps"],
                "tasks": constants["tasks"],
                "policies": constants["policies"],
            }
        )

    @staticmethod
    def funny_reply(query: str) -> str:
        # format chain
        prompt = hub.pull("sredeemer/joke")
        chain = prompt | Chain.llama3_str_parser()

        return chain.invoke({"question": query})
