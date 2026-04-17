import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.orm import Document, User
from app.schemas.document import DocumentResponse
from app.core.dependencies import RoleChecker, get_current_active_user
from app.services.document_service import save_upload_file, extract_text_from_pdf
from app.services.rag_service import index_document, delete_document_vectors

router = APIRouter(prefix="/documents", tags=["documents"])

analyst_plus = RoleChecker(["Admin", "Analyst"])
auditor_plus = RoleChecker(["Admin", "Analyst", "Auditor", "Client"])

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    title: str = Form(...),
    company_name: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db), 
    current_user: User = Depends(analyst_plus)
):
    document_id = str(uuid.uuid4())
    file_path = save_upload_file(file, document_id)
    
    new_doc = Document(
        document_id=document_id,
        title=title,
        company_name=company_name,
        document_type=document_type,
        uploaded_by=current_user.username,
        file_path=file_path
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    text = extract_text_from_pdf(file_path)
    if text:
        metadata = {
            "document_id": document_id,
            "title": title,
            "company_name": company_name,
            "document_type": document_type,
            "uploaded_by": current_user.username,
            "created_at": new_doc.created_at.isoformat()
        }
        index_document(document_id, text, metadata)
        
    return new_doc

@router.get("", response_model=List[DocumentResponse])
def get_all_documents(db: Session = Depends(get_db), current_user: User = Depends(auditor_plus)):
    return db.query(Document).all()

@router.get("/search", response_model=List[DocumentResponse])
def search_documents_by_metadata(
    company_name: Optional[str] = None,
    document_type: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(auditor_plus)
):
    query = db.query(Document)
    if company_name:
        query = query.filter(Document.company_name == company_name)
    if document_type:
        query = query.filter(Document.document_type == document_type)
    return query.all()

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db), current_user: User = Depends(auditor_plus)):
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db), current_user: User = Depends(analyst_plus)):
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
        
    db.delete(doc)
    db.commit()
    
    delete_document_vectors(document_id)
    return {"message": "Document deleted successfully"}
