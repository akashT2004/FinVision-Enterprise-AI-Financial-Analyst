from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.orm import User, Document
from app.schemas.rag import SearchQuery, SearchResult, AnalystResponse
from app.core.dependencies import RoleChecker
from app.services.rag_service import search_and_rerank, index_document
from app.services.document_service import extract_text_from_pdf
from app.services.analyst_agent import analyst_agent

router = APIRouter(prefix="/rag", tags=["rag"])
auditor_plus = RoleChecker(["Admin", "Analyst", "Auditor", "Client"])

@router.post("/search", response_model=List[SearchResult])
def perform_semantic_search(query: SearchQuery, current_user: User = Depends(auditor_plus)):
    results = search_and_rerank(query.query)
    return results

@router.post("/ask", response_model=AnalystResponse)
async def ask_analyst(query: SearchQuery, current_user: User = Depends(auditor_plus)):
    """
    Agentic RAG endpoint:
    1. Retrieve context via semantic search + reranking.
    2. Pass context to Gemini analyst.
    3. Generate answer and visualization data.
    """
    # 1. Retrieve 20 results for reranking, take top 12 for the agent for better table discovery
    context_chunks = search_and_rerank(query.query, top_k=12)
    
    if not context_chunks:
        raise HTTPException(status_code=404, detail="No relevant context found in documents.")
    
    # 2. Process with Agent
    response = await analyst_agent.analyze_and_respond(query.query, context_chunks)
    return response

@router.post("/index-document/{document_id}")
def manually_index_document(document_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker(["Admin", "Analyst"]))):
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    text = extract_text_from_pdf(doc.file_path)
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from document")
        
    metadata = {
        "document_id": document_id,
        "title": doc.title,
        "company_name": doc.company_name,
        "document_type": doc.document_type,
        "uploaded_by": doc.uploaded_by,
        "created_at": doc.created_at.isoformat()
    }
    index_document(document_id, text, metadata)
    return {"message": "Document indexed successfully"}

@router.get("/context/{document_id}")
def retrieve_document_context(document_id: str, current_user: User = Depends(auditor_plus)):
    from app.services.rag_service import qdrant_client, collection_name
    from qdrant_client.http import models
    response = qdrant_client.scroll(
        collection_name=collection_name,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.document_id",
                    match=models.MatchValue(value=document_id),
                )
            ]
        ),
        limit=20,
        with_payload=True
    )
    if response and response[0]:
        return {"chunks": [r.payload.get("page_content") for r in response[0]]}
    return {"chunks": []}

@router.delete("/remove-document/{id}")
def manually_remove_indices(id: str, current_user: User = Depends(RoleChecker(["Admin", "Analyst"]))):
    from app.services.rag_service import delete_document_vectors
    delete_document_vectors(id)
    return {"message": "Document vectors removed successfully"}
