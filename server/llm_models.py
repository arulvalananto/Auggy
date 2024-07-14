from langchain_community.llms import Ollama


def ollama_llama3():
    llm = Ollama(
        model="llama3"
    )
    return llm


def ollama_gemma2():
    llm = Ollama(
        model="gemma2"
    )
    return llm
