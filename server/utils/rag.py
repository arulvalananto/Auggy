import os

from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAG:
    @staticmethod
    def load_documents():
        if os.path.exists("./chroma_db"):
            return

        links = [
            "https://medium.com/munchy-bytes/exploring-langchain-ff13fff63340",
            "https://datastax.medium.com/what-is-langchain-b5583de2989a",
            "https://dev.to/shawonmajid/rag-techniques-multi-query-2p5h",
            "https://dev.to/rutamstwt/langchain-agents-22af",
        ]

        # load documents
        loader = WebBaseLoader(links)
        docs = loader.load()
        print(f"Loaded {len(docs)} documents")

        # split docs into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
        splits = text_splitter.split_documents(docs)
        print(f"Split {len(splits)} documents")

        # Embed documents
        db = Chroma.from_documents(
            embedding=HuggingFaceEmbeddings(),
            persist_directory="./chroma_db",
            collection_name="langchain",
            documents=splits,
        )

        return db

    @staticmethod
    def search_documents(query):
        db = Chroma(
            persist_directory="./chroma_db",
            collection_name="langchain",
            embedding_function=HuggingFaceEmbeddings(),
        )

        docs = db.similarity_search(query)

        return docs
