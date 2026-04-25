#!/usr/bin/env python3
"""
FastAPI Backend for Legal RAG System

REST API for legal Q&A with RAG pipeline.


Repository Setup: Initialize a GitHub repository and push the project.
   2. Fix start_api.sh: Update the script to properly activate the legal-rag/legalrag virtual
      environment before launching.
   3. Data Purge & Reload: The "Automated Extraction" approach should be abandoned for now.
      Stick to the "Manual Curation" strategy for the top 100-200 legal sections to ensure
      reliability.
   4. Severity Logic Update: Update severity_classifier.py to match the curated metadata
      fields.

"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "rag"))

from rag_pipeline import LegalRAGPipeline


# Pydantic models
class QueryRequest(BaseModel):
    """Request model for legal queries."""
    question: str = Field(..., min_length=5, max_length=500, description="Legal question")
    num_sources: Optional[int] = Field(5, ge=1, le=10, description="Number of sources to retrieve")
    include_metadata: Optional[bool] = Field(True, description="Include detailed metadata")


class Citation(BaseModel):
    """Citation model."""
    act: str
    section: str
    title: str
    text_snippet: str


class SeverityInfo(BaseModel):
    """Severity information model."""
    level: str
    reasoning: str
    confidence: float
    summary: Dict[str, str]


class QueryResponse(BaseModel):
    """Response model for legal queries."""
    question: str
    answer: str
    citations: List[Citation]
    severity: SeverityInfo
    num_sources: int
    disclaimer: str
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    database_status: str
    model_status: str


class StatsResponse(BaseModel):
    """Statistics response."""
    total_documents: int
    collection_name: str
    model_name: str
    uptime_seconds: float


# Initialize FastAPI app
app = FastAPI(
    title="Legal RAG API",
    description="REST API for Indian Legal Q&A System using RAG",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
rag_pipeline: Optional[LegalRAGPipeline] = None
start_time = datetime.now()


@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup."""
    global rag_pipeline
    
    print("Starting Legal RAG API...")
    print("="*60)
    
    try:
        # Check for OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  WARNING: OPENAI_API_KEY not set")
            print("Set it with: export OPENAI_API_KEY='your-key'")
        
        # Initialize pipeline
        rag_pipeline = LegalRAGPipeline(
            chroma_persist_dir="legal-rag/data/chroma_db",
            collection_name="indian_laws",
            model_name="gpt-4-turbo"
        )
        
        print("✓ RAG Pipeline initialized")
        print("✓ API ready to accept requests")
        print("="*60)
        
    except Exception as e:
        print(f"✗ Error initializing pipeline: {e}")
        print("API will start but queries will fail")
        rag_pipeline = None


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "Legal RAG API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    database_status = "healthy" if rag_pipeline and rag_pipeline.vectorstore else "unavailable"
    model_status = "healthy" if rag_pipeline and rag_pipeline.llm else "unavailable"
    
    return HealthResponse(
        status="healthy" if rag_pipeline else "degraded",
        timestamp=datetime.now().isoformat(),
        database_status=database_status,
        model_status=model_status
    )


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics."""
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    try:
        # Get collection stats
        collection = rag_pipeline.vectorstore._collection
        doc_count = collection.count()
        
        uptime = (datetime.now() - start_time).total_seconds()
        
        return StatsResponse(
            total_documents=doc_count,
            collection_name=rag_pipeline.collection_name,
            model_name=rag_pipeline.model_name,
            uptime_seconds=uptime
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Ask a legal question.
    
    Args:
        request: QueryRequest with question
        
    Returns:
        QueryResponse with answer, citations, and severity
    """
    if not rag_pipeline:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline not initialized. Check server logs."
        )
    
    try:
        # Process query
        response = rag_pipeline.query(request.question)
        
        # Add timestamp
        response["timestamp"] = datetime.now().isoformat()
        
        return QueryResponse(**response)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/search")
async def search_documents(
    query: str = Query(..., min_length=3, max_length=200),
    k: int = Query(5, ge=1, le=20)
):
    """
    Search for relevant legal documents.
    
    Args:
        query: Search query
        k: Number of results
        
    Returns:
        List of relevant documents
    """
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    try:
        docs = rag_pipeline.retrieve_relevant_chunks(query, k=k)
        
        results = []
        for doc in docs:
            results.append({
                "text": doc.page_content,
                "metadata": doc.metadata,
                "section": f"{doc.metadata.get('document_type', 'unknown').upper()} - Section {doc.metadata.get('section_number', 'unknown')}",
                "title": doc.metadata.get('section_title', '')
            })
        
        return {
            "query": query,
            "num_results": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")


@app.get("/acts")
async def list_acts():
    """
    List available legal acts in the database.
    
    Returns:
        List of acts
    """
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    try:
        # Sample documents to get unique acts
        collection = rag_pipeline.vectorstore._collection
        sample = collection.peek(limit=100)
        
        acts = set()
        if sample and 'metadatas' in sample:
            for metadata in sample['metadatas']:
                doc_type = metadata.get('document_type', 'unknown')
                acts.add(doc_type)
        
        return {
            "acts": sorted(list(acts)),
            "total_acts": len(acts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing acts: {str(e)}")


def main():
    """Run the API server."""
    print("Starting Legal RAG API Server...")
    print("="*60)
    print("Make sure:")
    print("1. ChromaDB is populated (run vector_store.py)")
    print("2. OPENAI_API_KEY is set: export OPENAI_API_KEY='your-key'")
    print("="*60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
