from typing import Union
from langchain_community.llms import Ollama

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat():
    llm = Ollama(
        model="llama3"
    )  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `

    return llm.invoke("Tell me a joke")