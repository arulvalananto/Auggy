import json
from langchain import hub
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import Question
from llm_models import ollama_llama3
from doc_loaders import notion_db_loader
from prompt_templates import (
    generate_correction_template,
    generate_JSON_formatter_template
)


load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    """
    A simple endpoint that returns a JSON greeting.
    """
    return {"Hello": "World"}


@app.post("/chat")
def chat():
    """
    An endpoint that uses an LLM (Large Language Model) to generate a response to "Tell me a joke".
    """
    llm = ollama_llama3()
    return llm.invoke("Tell me a joke")


@app.get('/notion_loader')
def notion_doc_loader():
    """
    An endpoint that loads documents from a Notion database using a custom loader.
    """
    loader = notion_db_loader()
    docs = loader.load()
    return docs


@app.get('/index_doc')
def index_doc():
    """
    An endpoint that loads documents from a Notion database, splits them into chunks for processing,
    and prints the chunks. Embedding and retrieval functionality is commented out.
    """
    # load documents
    loader = WebBaseLoader(["https://lilianweng.github.io/posts/2023-06-23-agent/"])
    docs = loader.load()
    print(f'Loaded {len(docs)} documents')
    
    # split docs into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100, 
        chunk_overlap=20
    )
    splits = text_splitter.split_documents(docs)
    print(f'Split {len(splits)} documents')

    # Embed
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=HuggingFaceEmbeddings()
    )
    retriever = vectorstore.as_retriever()
    print('Indexed documents')

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")
    
    # LLM
    llm = ollama_llama3()

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

@app.post('/json_formatter_prompt')
def prompt_template(question_payload: Question):
    question = question_payload.question
    
    # templates
    correction_template = generate_correction_template()
    json_format_template = generate_JSON_formatter_template()
    
    # Prompt
    correction_prompt = ChatPromptTemplate.from_template(correction_template)
    json_format_prompt = ChatPromptTemplate.from_template(json_format_template)
    
    # LLM
    llm = ollama_llama3()
    
    # chains
    correct_chain = (correction_prompt | llm | StrOutputParser())
    format_chain = (json_format_prompt | llm | StrOutputParser())
     
    # combine chains    
    rag_chains = correct_chain | format_chain 
    
    # invoke
    answer = rag_chains.invoke({"question": question})
    
    return {"question": question, "answer": json.loads(answer)}