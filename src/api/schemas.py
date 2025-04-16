from typing import Dict
from pydantic import BaseModel


class ResultsPayload(BaseModel):
    chat_id: int
    results: Dict[str, float]
