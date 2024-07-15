from fastapi import FastAPI
from dotenv import load_dotenv

from utils.rag import RAG
from routers import test, chat

load_dotenv()

# load documents and store in vector db
RAG.load_documents()

app = FastAPI()

app.include_router(test.router)
app.include_router(chat.router)
