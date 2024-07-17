from pydantic import BaseModel, Field


class AddLog(BaseModel):
    hours: str = Field(description="The hours spent on the task")
    task_name: str = Field(
        description="The name of the task", examples=["RAV-50", "WI-12"]
    )
    project_name: str = Field(description="The name of the project")
    date: str = Field(description="It is a date if date is not exist consider as None", examples=['today', 'yesterday', '2022-12-12'])
