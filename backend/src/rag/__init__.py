"""
Legal RAG System - RAG Module

Core RAG components for legal document retrieval and generation.
"""

from .chunker import TextChunker
from .embedder import LegalEmbedder
from .vector_store import LegalVectorStore
from .severity_classifier import SeverityClassifier, SeverityLevel
from .rag_pipeline import LegalRAGPipeline

__all__ = [
    'TextChunker',
    'LegalEmbedder',
    'LegalVectorStore',
    'SeverityClassifier',
    'SeverityLevel',
    'LegalRAGPipeline'
]
