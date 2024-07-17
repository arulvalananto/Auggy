from typing import List, Union

from fastapi import UploadFile
from models.common import Classification
from utils.integration import Integration
from utils.enums import Category
from utils.files import Files
from utils.query import Query
from utils.task import Task


class LogicalRoute:
    @staticmethod
    def classification_route(
        question: str,
        classification: Classification,
        files: Union[List[UploadFile] | None],
    ):
        if files is not None:
            return Files.process(question, files)
        else:
            # check the category of the classification
            if Category.APP.value in classification["category"].lower():
                return Integration.process(question, classification)
            elif Category.TASK.value in classification["category"].lower():
                return Task.process(question)
            else:
                return Query.process(question)
