from enums import Category
from fastapi import APIRouter
from models import Question
from utils.chains import Chain
from utils.rag import RAG

router = APIRouter(prefix="/chat", tags=["basic"])


@router.post("/prompt")
def chat_prompt(payload: Question):
    question = payload.query

    # format question prompt
    query = Chain.format_user_query(question)

    # classify user's query
    classification = Chain.classify_query(query)
    response = None

    if classification["category"].lower() == Category.APP.value:
        # perform app related tasks here.
        print("app")
    elif classification["category"].lower() == Category.QUERY.value:
        # perform query related tasks here.
        response = RAG.search_documents(question)
    elif classification["category"].lower() == Category.TASK.value:
        # perform task like image generation and text generation here.
        print("task")
    else:
        response = Chain.funny_reply(query)

    return {
        "question": question,
        "formatted_question": query,
        "classification": classification,
        "response": response,
    }
