from fastapi import APIRouter

from models import Question
from utils.chains import Chain

router = APIRouter(prefix="/chat", tags=["basic"])


@router.post("/prompt")
def chat_prompt(payload: Question):
    question = payload.query

    # format question prompt
    query = Chain.format_user_query(question)

    # classify user's query
    classification = Chain.classify_query(query)

    return {
        "question": question,
        "formatted_question": query,
        "classification": classification,
    }
