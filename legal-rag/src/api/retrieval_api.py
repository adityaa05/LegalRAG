#!/usr/bin/env python3
"""
Retrieval-Only API - Works without LLM

Returns relevant legal sections without AI-generated answers.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from sentence_transformers import SentenceTransformer
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "rag"))
from severity_classifier import SeverityClassifier

app = FastAPI(
    title="Legal Retrieval API",
    description="Semantic search over Indian legal documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
embedder = None
chroma_client = None
collection = None
severity_classifier = None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    global embedder, chroma_client, collection, severity_classifier
    
    print("Loading embedding model...")
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    print("Connecting to ChromaDB...")
    # Use absolute path from project root
    db_path = Path(__file__).parent.parent.parent / "data" / "chroma_db"
    chroma_client = chromadb.PersistentClient(path=str(db_path))
    collection = chroma_client.get_collection("indian_laws")
    
    print("Initializing severity classifier...")
    severity_classifier = SeverityClassifier()
    
    print(f"✓ Ready! Database has {collection.count()} documents")


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    num_results: int = Field(5, ge=1, le=20)


class SearchResult(BaseModel):
    text: str
    act: str
    section: str
    title: str
    severity: str
    similarity: float
    metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    num_results: int
    timestamp: str


@app.get("/")
async def root():
    return {
        "message": "Legal Retrieval API",
        "status": "operational",
        "documents": collection.count() if collection else 0,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "connected" if collection else "disconnected",
        "documents": collection.count() if collection else 0
    }


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search for relevant legal sections.
    
    Returns raw legal text without AI-generated answers.
    """
    if not collection or not embedder:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        # Generate query embedding
        query_embedding = embedder.encode(
            request.query,
            normalize_embeddings=True
        ).tolist()
        
        # Search ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=request.num_results
        )
        
        # Format results
        search_results = []
        for i in range(len(results['documents'][0])):
            metadata = results['metadatas'][0][i]
            
            # Classify severity
            severity_level, reasoning, confidence = severity_classifier.classify(metadata)
            
            search_results.append(SearchResult(
                text=results['documents'][0][i],
                act=metadata.get('document_type', 'unknown').upper(),
                section=metadata.get('section_number', 'unknown'),
                title=metadata.get('section_title', ''),
                severity=severity_level.value,
                similarity=1 - results['distances'][0][i],
                metadata=metadata
            ))
        
        return SearchResponse(
            query=request.query,
            results=search_results,
            num_results=len(search_results),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.get("/stats")
async def stats():
    """Get database statistics."""
    if not collection:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    return {
        "total_documents": collection.count(),
        "collection_name": collection.name
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
