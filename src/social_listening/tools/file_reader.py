import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FileReaderInput(BaseModel):
    file_path: str = Field(..., description="Path to the file to read")

class FileReaderTool(BaseTool):
    name: str = "Safe File Reader"
    description: str = "Safely reads file content, returns empty string if file doesn't exist"
    args_schema: Type[BaseModel] = FileReaderInput

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"File {file_path} does not exist yet. Please wait for previous tasks to complete."
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file {file_path}: {str(e)}"