from pydantic import BaseModel
from typing import List

# Pydantic model to validate incoming requests
class TextRequest(BaseModel):
    text: str
    entities: List[str] = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]
    language: str = "en"
