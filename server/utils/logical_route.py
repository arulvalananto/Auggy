from typing import List, Union

from fastapi import UploadFile
from models import Classification
from utils.apps import Apps
from utils.chains import Chain
from utils.rag import RAG
from utils.task import Task
from utils.enums import Category
from utils.files import Files


class LogicalRoute:
    @staticmethod
    def classification_route(question: str, classification: Classification, files: Union[List[UploadFile] | None]):
        if files is not None:
            return Files.perform_action(question, files)
        else:        
            if Category.APP.value in classification["category"].lower():
                return Apps.find_app_and_action_type(question)
            elif Category.QUERY.value in classification["category"].lower():
                return RAG.search_documents(question)
            elif Category.TASK.value in classification["category"].lower():
                return Task.generate_response(question)
            else:
                return Chain.funny_reply(question)
