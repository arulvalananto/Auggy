import json

from fastapi import APIRouter

from langchain import hub
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

router = APIRouter(prefix="/basic", tags=["basic"])


@router.post("/chat")
def chat():
    """
    An endpoint that uses an LLM (Large Language Model) to generate a response
    to "Tell me a joke".
    """
    llm = LanguageModels.ollama_gemma2()
    return llm.invoke("Tell me a joke")


@router.get("/notion_loader")
def notion_doc_loader():
    """
    An endpoint that loads documents from a Notion database using a custom
    loader.
    """
    loader = DocumentLoaders.notion_db_loader()
    docs = loader.load()
    return docs


@router.get("/index_doc")
def index_doc():
    """
    An endpoint that loads documents from a Notion database, splits them into
    chunks for processing, and prints the chunks. Embedding and retrieval
    functionality is commented out.
    """
    # load documents
    loader = WebBaseLoader(["https://lilianweng.github.io/posts/2023-06-23-agent/"])
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")
    # split docs into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    splits = text_splitter.split_documents(docs)
    print(f"Split {len(splits)} documents")

    # Embed
    vectorstore = Chroma.from_documents(
        documents=splits, embedding=HuggingFaceEmbeddings()
    )
    retriever = vectorstore.as_retriever()
    print("Indexed documents")

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")

    # LLM
    llm = LanguageModels.ollama_gemma2()

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Question
    return rag_chain.invoke("What is Task Decomposition?")


@router.post("/json_formatter_prompt")
def prompt_template(payload: Question):
    question = payload.question

    # prompt templates
    correction_template = PromptTemplatesGenerator.improve_query()
    app_finder_template = PromptTemplatesGenerator.app_and_action_finder()

    # Prompt construction
    correction_prompt = ChatPromptTemplate.from_template(correction_template)
    app_finder_prompt = ChatPromptTemplate.from_template(app_finder_template)

    # LLM
    llm = LanguageModels.ollama_llama3()

    # chains
    correct_chain = correction_prompt | llm | StrOutputParser()
    finder_chain = app_finder_prompt | llm | StrOutputParser()

    # combine chains
    rag_chains = correct_chain | finder_chain

    # invoke
    answer = rag_chains.invoke({"question": question})
    print(f"answer: {answer}")
    formatted_answer = json.loads(answer)
    print(f"formatted answer: {formatted_answer}")
    return {"question": question, "answer": formatted_answer}
