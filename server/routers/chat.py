from typing import Annotated, List, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
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
        print(f"\nQuestion formatted: {query}\n")

        if files is not None:
            response = Files.process(question, files)
            classification = None
        else:
            # classify user's query
            classification = Chain.classify_query(question)
            print(f"\nQuery classified: {classification}\n")

            response = LogicalRoute.classification_route(
                question=question, classification=classification, files=files
            )

        return JSONResponse(
            content={
                "response": response,
                "processed_data": {
                    "question_correction_details": query,
                    "classification_details": classification,
                },
            },
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            e=e,
            message="An unexpected error occurred. Please try again later.",
        )
