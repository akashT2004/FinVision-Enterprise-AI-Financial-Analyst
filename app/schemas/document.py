from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    company_name: str
    document_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    document_id: str
    uploaded_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True
