from langchain_community.llms import Ollama


class LanguageModels:
    @staticmethod
    def ollama_llama3():
        llm = Ollama(model="llama3")
        return llm

    @staticmethod
    def ollama_gemma2():
        llm = Ollama(model="gemma2")
        return llm
