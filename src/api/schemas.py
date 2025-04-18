from typing import Dict
from pydantic import BaseModel


class ChatidAndResults(BaseModel):
    chat_id: int
    results: Dict[str, float]

    class Config:
        json_schema_extra = {
            "example": {
                "chat_id": 123456789,
                "results": {
                    "Food": 25.00,
                    "Transport": 10.50,
                    "Итого": 35.50
                }
            }
        }


class Response(BaseModel):
    status: str
    chat_id: int

    class Config:
        json_schema_extra = {
            "example": {"status": "success", "chat_id": 123456789}
        }
