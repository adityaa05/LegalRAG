"""
Legal RAG System - Ingestion Module

PDF processing and text extraction for legal documents.
"""

from .pdf_processor import LegalDocProcessor
from .batch_processor import BatchLegalProcessor

__all__ = [
    'LegalDocProcessor',
    'BatchLegalProcessor'
]
