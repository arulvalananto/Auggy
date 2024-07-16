from typing import Annotated, List, Optional, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from models import Question
from utils.chains import Chain
from utils.files import Files
from utils.logical_route import LogicalRoute

router = APIRouter(prefix="/chat", tags=["basic"])


@router.post("/prompt")
def chat_prompt(
    question: Annotated[str, Form()],
    files: List[Union[UploadFile, None]] = File(None),
):
    try:
        # format question prompt
        query = Chain.improve_query(question)
        print(f"Question formatted: {query}")  # After formatting the question

        # classify user's query
        classification = Chain.classify_query(question)
        print(f"Query classified: {classification}")  # After classifying the query

        response = LogicalRoute.classification_route(
            question=question, classification=classification, files=files
        )

        return JSONResponse(content={"response": response}, status_code=200)
    except Exception as e:
        print("An unexpected error occurred. Please try again later.", e)
        raise HTTPException(
            status_code=500,
            message="An unexpected error occurred. Please try again later.",
        )


@router.post("/uploadfiles/")
async def create_upload_files(files: List[Union[UploadFile, None]] = File(None)):
    return {"filenames": [file.filename for file in files]}
