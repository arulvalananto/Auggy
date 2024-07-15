from fastapi import FastAPI
from dotenv import load_dotenv

from routers import test, chat

load_dotenv()

app = FastAPI()

app.include_router(test.router)
app.include_router(chat.router)
