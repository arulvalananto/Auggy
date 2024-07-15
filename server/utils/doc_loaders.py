import os
from langchain_community.document_loaders import NotionDBLoader

class DocumentLoaders:
    @staticmethod
    def notion_db_loader():
        NOTION_TOKEN = os.environ["NOTION_AUTH_SECRET"]
        DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

        # create a loader
        loader = NotionDBLoader(
            integration_token=NOTION_TOKEN,
            database_id=DATABASE_ID,
            request_timeout_sec=30,  # optional, defaults to 10
        )
        return loader
