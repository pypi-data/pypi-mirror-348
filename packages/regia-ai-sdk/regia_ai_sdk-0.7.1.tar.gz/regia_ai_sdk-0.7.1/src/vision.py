
import requests
import json
import time
import base64
import os
from typing import Dict, Union, Optional, Type
from pydantic import BaseModel


class VisionClient:
    def __init__(self, token: str, base_url: str = "https://api.regia.cloud/v1"):
        self.token = token
        self.base_url = base_url.rstrip("/")

    def extract(
        self,
        file: Union[str, bytes],
        schema: Union[Dict, Type[BaseModel]],
        filename: str = "document.pdf",
        mime_type: str = "application/pdf"
    ) -> Dict:
        """
        Submits a PDF and schema to the extractor API.
        file: str (file path or base64) or bytes
        schema: dict or Pydantic model
        """
        # Process schema
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            schema_payload = self._pydantic_to_extraction_schema(schema)
        elif isinstance(schema, dict):
            schema_payload = schema
        else:
            raise ValueError(
                "Schema must be a dict or a Pydantic BaseModel class.")

        # Read file content
        if isinstance(file, str):
            if os.path.exists(file):
                with open(file, "rb") as f:
                    file_bytes = f.read()
            else:
                try:
                    file_bytes = base64.b64decode(file)
                except Exception:
                    raise ValueError("Invalid file path or base64 string.")
        elif isinstance(file, bytes):
            file_bytes = file
        else:
            raise ValueError(
                "File must be a valid path, bytes, or base64 string.")

        files = {
            "pdf_file": (filename, file_bytes, mime_type),
            "schema": ("schema.json", json.dumps(schema_payload), "application/json")
        }

        response = requests.post(
            f"{self.base_url}/vision/extract",
            files=files,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        response.raise_for_status()
        return response.json()

    def _pydantic_to_extraction_schema(self, model: Type[BaseModel]) -> dict:
        """
        Converts a Pydantic model to JSON Schema
        """
        return model.model_json_schema()

