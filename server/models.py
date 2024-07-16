from pydantic import BaseModel, Field

class Question(BaseModel):
    query: str


class Classification(BaseModel):
    category: str = Field(description="The category of the classification")
    reason: str = Field(description="The reason for the classification")
