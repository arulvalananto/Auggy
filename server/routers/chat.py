from fastapi import APIRouter

from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.models import Question
from utils.llm_models import LanguageModels
from utils.doc_loaders import DocumentLoaders
from utils.prompt_templates import PromptTemplatesGenerator

router = APIRouter(prefix="/chat", tags=["basic"])


@router.post("/prompt")
def chat_prompt(payload: Question):
    question = payload.question

    # format question prompt
    prompt = ChatPromptTemplate.from_template(
        Prompt_Templates_Generator.improve_query()
    )

    # LLM
    llm = LanguageModels.ollama_llama3()

    # format chain
    chain = prompt | llm | StrOutputParser()

    # invoke
    answer = chain.invoke({"question": question})

    return {"question": question, "answer": answer}
