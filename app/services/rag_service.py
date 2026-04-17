import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import CrossEncoder

from app.core.config import settings

qdrant_client = QdrantClient(path=settings.QDRANT_PATH)

embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

collection_name = "financial_docs"

try:
    qdrant_client.get_collection(collection_name)
except Exception:
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=collection_name,
    embedding=embeddings,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def index_document(document_id: str, text: str, metadata: dict):
    chunks = text_splitter.create_documents([text], metadatas=[metadata])
    vector_store.add_documents(chunks)

def search_and_rerank(query: str, top_k: int = 5, top_n_retrieve: int = 20):
    docs = vector_store.similarity_search(query, k=top_n_retrieve)
    
    if not docs:
        return []

    pairs = [[query, doc.page_content] for doc in docs]
    scores = reranker.predict(pairs)
    
    scored_docs = zip(scores, docs)
    sorted_docs = sorted(scored_docs, key=lambda x: x[0], reverse=True)
    
    results = []
    for score, doc in sorted_docs[:top_k]:
        results.append({
            "document_id": doc.metadata.get("document_id", "unknown"),
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": float(score)
        })
    return results

def delete_document_vectors(document_id: str):
    from qdrant_client.http import models
    qdrant_client.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.document_id",
                        match=models.MatchValue(value=document_id),
                    )
                ]
            )
        )
    )
