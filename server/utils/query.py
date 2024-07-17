from utils.chains import Chain
from utils.rag import RAG


class Query:
    @staticmethod
    def process(question: str) -> str:
        docs = RAG.search_documents(question)

        rag_chain = Chain.rag_search()

        # Post-processing
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        sources = [
            {
                "description": doc.metadata["description"],
                "source": doc.metadata["source"],
            }
            for doc in docs
        ]

        answer = rag_chain.invoke({"context": format_docs(docs), "question": question})

        # verify answer
        verifier_chain = Chain.verify_answer()
        validation = verifier_chain.invoke({"question": question, "answer": answer})
        if validation["is_valid"] == "no":
            answer = Chain.funny_reply().invoke({"question": question})
            sources = []

        return {
            "collected_docs": len(docs),
            "answer": answer,
            "is_valid": validation["is_valid"],
            "sources": sources,
        }
