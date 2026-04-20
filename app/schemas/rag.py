from pydantic import BaseModel
from typing import List, Any, Optional, Dict

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    document_id: str
    content: str
    score: float
    metadata: dict

class Citation(BaseModel):
    doc_id: str
    content_snippet: str

class ChartDataItem(BaseModel):
    label: str
    value: Optional[float] = None
    values: Optional[Dict[str, float]] = None

class AnalystResponse(BaseModel):
    answer: str
    has_chart: bool
    chart_type: Optional[str] = None
    chart_data: List[ChartDataItem] = []
    citations: List[Citation] = []
