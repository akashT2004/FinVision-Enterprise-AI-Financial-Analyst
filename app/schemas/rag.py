from pydantic import BaseModel
from typing import List, Any

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    document_id: str
    content: str
    score: float
    metadata: dict
