from pydantic import BaseModel


class Question(BaseModel):
    query: str

class Classification(BaseModel):
    category: str
    reason: str