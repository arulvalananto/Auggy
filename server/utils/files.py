import os
import uuid
from typing import List

from fastapi import UploadFile
from langchain_community.document_loaders import BSHTMLLoader, PyPDFLoader, TextLoader


class Files:
    @staticmethod
    def load_docs(files: List[UploadFile]):
        docs = []

        # Ensure the uploads directory exists
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)

        for file in files:
            # Save the file temporarily
            myuuid = uuid.uuid4()
            ext = file.filename.split(".")[-1]
            tmp_location = os.path.join(uploads_dir, f"{myuuid}{ext}")

            # Save the file
            with open(tmp_location, "wb") as f:
                f.write(file.file.read())

            # Load the file
            if file.content_type == "application/pdf":
                loader = PyPDFLoader(tmp_location)
                docs.extend(loader.load_and_split())
            elif file.content_type == "text/plain":
                loader = TextLoader(tmp_location)
                docs.extend(loader.load())

            # Remove the temporary file
            os.remove(tmp_location)

        return docs

    @staticmethod
    def perform_action(question: str, files: List[UploadFile]):
        # Perform load docs based on the file type
        docs = Files.load_docs(files)

        print(f"Docs loaded: {docs}")

        return {
            "files": [file.filename for file in files],
            "message": "Files uploaded successfully.",
        }
