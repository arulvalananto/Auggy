from langchain import hub
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from models.common import Classification, Verifier
from utils.constants import constants
from utils.llm_models import LanguageModels
from utils.prompt_templates import PromptTemplatesGenerator


class Chain:

    def improve_query(question: str) -> str:
        prompt = hub.pull("promptcyril/fix_spelling_and_grammar")

        # LLM
        llm = LanguageModels.ollama_llama3()

        chain = prompt | llm | StrOutputParser()

        return chain.invoke({"text": question, "accent": "professional"})

    @staticmethod
    def classify_query(question: str) -> Classification:
        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=Classification)

        prompt = PromptTemplate(
            template=PromptTemplatesGenerator.classify_query(),
            input_variables=["question", "apps", "tasks", "policies"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | parser

        return chain.invoke(
            {
                "question": question,
                "apps": constants["apps"],
                "tasks": constants["tasks"],
                "policies": constants["policies"],
            }
        )

    @staticmethod
    def funny_reply():
        # format chain
        prompt = hub.pull("sredeemer/joke")

        # LLM
        llm = LanguageModels.ollama_llama3()

        chain = prompt | llm | StrOutputParser()

        return chain

    @staticmethod
    def rag_search():
        # prompt
        # https://smith.langchain.com/hub/rlm/rag-prompt
        prompt = hub.pull("rlm/rag-prompt")

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | StrOutputParser()

        return chain

    @staticmethod
    def verify_answer():
        parser = JsonOutputParser(pydantic_object=Verifier)

        prompt = PromptTemplate(
            template=PromptTemplatesGenerator.double_verifier(),
            input_variables=["question", "answer"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | parser

        return chain

    @staticmethod
    def payload_formatter(template):
        parser = JsonOutputParser(pydantic_object=template)

        prompt = PromptTemplate(
            template=PromptTemplatesGenerator.payload_formatter(),
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        llm = LanguageModels.ollama_llama3()

        chain = prompt | llm | parser

        return chain

    @staticmethod
    def file_handler():
        # prompt
        # https://smith.langchain.com/hub/rlm/rag-prompt
        prompt = ChatPromptTemplate.from_template(
            template=PromptTemplatesGenerator.file_handler()
        )

        # LLM
        llm = LanguageModels.ollama_llama3()

        # format chain
        chain = prompt | llm | StrOutputParser()

        return chain
