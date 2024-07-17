from pydantic import BaseModel, Field
from utils.enums import Valid


class Question(BaseModel):
    query: str


class Classification(BaseModel):
    category: str = Field(description="The category of the classification")
    reason: str = Field(description="The reason for the classification")
    app_name: str | None = Field(
        description="The name of the application if category is app"
    )
    action_name: str | None = Field(
        description="The name of application's action if category is app"
    )
    task_name: str | None = Field(
        description="The name of the task if category is task"
    )


class Verifier(BaseModel):
    is_valid: Valid = Field(description="The validity of the answer")
