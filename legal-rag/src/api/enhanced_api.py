#!/usr/bin/env python3
"""
Enhanced Legal RAG API - Situation Analysis

Analyzes legal situations and provides comprehensive results.
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
import re

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "rag"))
from severity_classifier import SeverityClassifier, SeverityLevel

app = FastAPI(
    title="Enhanced Legal Analysis API",
    description="Situation-based legal analysis for Indian law",
    version="2.0.0"
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
    # Use the manual curated database
    db_path = Path(__file__).parent.parent.parent / "data" / "chroma_db_production"
    chroma_client = chromadb.PersistentClient(path=str(db_path))
    collection = chroma_client.get_collection("indian_laws")
    
    print("Initializing severity classifier...")
    severity_classifier = SeverityClassifier()
    
    print(f"✓ Ready! Database has {collection.count()} documents")


class SituationRequest(BaseModel):
    situation: str = Field(..., min_length=10, max_length=2000, description="Describe your legal situation")
    num_results: int = Field(10, ge=5, le=20, description="Number of relevant laws to retrieve")


class LegalSection(BaseModel):
    act: str
    section: str
    title: str
    text: str
    severity: str
    severity_icon: str
    similarity: float
    applies_if: str


class SituationAnalysis(BaseModel):
    situation_summary: str
    key_legal_terms: List[str]
    relevant_laws: List[LegalSection]
    overall_severity: str
    severity_explanation: str
    key_factors: List[str]
    recommendations: List[str]
    disclaimer: str
    timestamp: str


def extract_legal_keywords(situation: str) -> List[str]:
    """Extract legal keywords from situation description."""
    # Common legal terms
    legal_terms = {
        'accident': ['accident', 'collision', 'crash', 'hit'],
        'death': ['death', 'die', 'fatal', 'killed', 'deceased'],
        'injury': ['injured', 'hurt', 'wounded', 'harm'],
        'negligence': ['negligent', 'careless', 'rash', 'reckless'],
        'driving': ['driving', 'vehicle', 'car', 'bike', 'scooty', 'motor'],
        'intention': ['intentional', 'deliberate', 'willful', 'knowingly'],
        'property': ['property', 'damage', 'destruction'],
        'theft': ['theft', 'stolen', 'robbery', 'burglary'],
        'assault': ['assault', 'attack', 'violence', 'fight'],
        'fraud': ['fraud', 'cheat', 'deceive', 'scam']
    }
    
    situation_lower = situation.lower()
    found_terms = []
    
    for category, terms in legal_terms.items():
        if any(term in situation_lower for term in terms):
            found_terms.append(category)
    
    return found_terms


def generate_search_queries(situation: str, keywords: List[str]) -> List[str]:
    """Generate multiple search queries from situation."""
    queries = []
    
    # Original situation
    queries.append(situation)
    
    # Keyword-based queries
    if 'accident' in keywords and 'death' in keywords:
        queries.append("causing death by negligence vehicular accident punishment")
        queries.append("culpable homicide not amounting to murder accident")
    
    if 'accident' in keywords and 'injury' in keywords:
        queries.append("causing hurt by rash negligent act punishment")
        queries.append("vehicular accident injury legal consequences")
    
    if 'negligence' in keywords and 'driving' in keywords:
        queries.append("rash and negligent driving public way punishment")
        queries.append("dangerous driving motor vehicle act penalties")
    
    if 'death' in keywords:
        queries.append("death caused by accident legal liability")
    
    if 'injury' in keywords:
        queries.append("grievous hurt simple hurt punishment")
    
    # Add general query
    queries.append(" ".join(keywords) + " punishment legal consequences")
    
    return queries[:5]  # Limit to 5 queries


def determine_overall_severity(sections: List[Dict[str, Any]]) -> tuple:
    """Determine overall severity from multiple sections."""
    severity_scores = {'RED': 3, 'YELLOW': 2, 'GREEN': 1, 'UNKNOWN': 0}
    
    if not sections:
        return 'UNKNOWN', 'No relevant laws found'
    
    # Get highest severity
    max_severity = 'GREEN'
    max_score = 0
    
    for section in sections:
        severity = section.get('severity', 'UNKNOWN')
        score = severity_scores.get(severity, 0)
        if score > max_score:
            max_score = score
            max_severity = severity
    
    explanations = {
        'RED': 'High severity - Serious criminal offense with severe penalties (10+ years, life imprisonment, or death penalty). Non-bailable.',
        'YELLOW': 'Moderate severity - Criminal offense with moderate penalties (3-10 years imprisonment). May be bailable.',
        'GREEN': 'Low severity - Minor offense with low penalties (<3 years or fine only). Usually bailable.',
        'UNKNOWN': 'Severity unclear - Insufficient information to determine exact penalties.'
    }
    
    return max_severity, explanations.get(max_severity, '')


def generate_recommendations(severity: str, keywords: List[str]) -> List[str]:
    """Generate recommendations based on severity and situation."""
    recommendations = []
    
    if severity == 'RED':
        recommendations.append("🚨 URGENT: Consult a criminal defense lawyer IMMEDIATELY")
        recommendations.append("Do NOT give any statements to police without lawyer present")
        recommendations.append("Preserve all evidence (photos, videos, witness contacts)")
        recommendations.append("File FIR if you haven't already")
        recommendations.append("Do not leave the jurisdiction without informing authorities")
    
    elif severity == 'YELLOW':
        recommendations.append("⚠️ Consult a lawyer as soon as possible")
        recommendations.append("File/obtain copy of FIR")
        recommendations.append("Collect evidence and witness statements")
        recommendations.append("Consider anticipatory bail if applicable")
        recommendations.append("Cooperate with investigation but with legal counsel")
    
    elif severity == 'GREEN':
        recommendations.append("✓ Legal consultation recommended")
        recommendations.append("File complaint/FIR if needed")
        recommendations.append("Maintain records of all documents")
        recommendations.append("May be resolved through legal procedures")
    
    # Situation-specific recommendations
    if 'accident' in keywords:
        recommendations.append("Report accident to police within 24 hours")
        recommendations.append("Get medical examination report for injuries")
        recommendations.append("Inform insurance company immediately")
    
    if 'death' in keywords:
        recommendations.append("Expect police investigation and possible arrest")
        recommendations.append("Do not tamper with evidence or leave scene")
    
    if 'negligence' in keywords:
        recommendations.append("Gather evidence proving you were not negligent")
        recommendations.append("Get witness statements supporting your version")
    
    return recommendations


def identify_key_factors(situation: str, keywords: List[str]) -> List[str]:
    """Identify key legal factors from situation."""
    factors = []
    
    if 'accident' in keywords:
        factors.append("Who had right of way at the intersection?")
        factors.append("Were traffic signals followed?")
        factors.append("Speed of vehicles involved")
        factors.append("Road conditions and visibility")
    
    if 'negligence' in keywords:
        factors.append("Was there rash or negligent driving?")
        factors.append("Were traffic rules violated?")
        factors.append("Could the accident have been avoided?")
    
    if 'death' in keywords or 'injury' in keywords:
        factors.append("Severity of injuries/death")
        factors.append("Medical reports and autopsy (if applicable)")
        factors.append("Time taken to provide medical assistance")
    
    if 'intention' in keywords:
        factors.append("Was there intent to cause harm?")
        factors.append("Was it accidental or deliberate?")
    
    factors.append("Witness testimonies")
    factors.append("CCTV footage or dashcam evidence")
    factors.append("Police investigation findings")
    
    return factors


@app.post("/analyze", response_model=SituationAnalysis)
async def analyze_situation(request: SituationRequest):
    """
    Analyze a legal situation and provide comprehensive results.
    
    Takes a situation description and returns relevant laws, severity analysis,
    and recommendations.
    """
    if not collection or not embedder:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        situation = request.situation
        
        # Extract keywords
        keywords = extract_legal_keywords(situation)
        
        # Generate search queries
        search_queries = generate_search_queries(situation, keywords)
        
        # Search for each query and collect results
        all_results = {}
        
        for query in search_queries:
            query_embedding = embedder.encode(query, normalize_embeddings=True).tolist()
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=request.num_results
            )
            
            # Add to results (deduplicate by chunk_id)
            for i in range(len(results['documents'][0])):
                metadata = results['metadatas'][0][i]
                chunk_id = metadata.get('chunk_id', f'unknown_{i}')
                
                if chunk_id not in all_results:
                    all_results[chunk_id] = {
                        'text': results['documents'][0][i],
                        'metadata': metadata,
                        'distance': results['distances'][0][i],
                        'similarity': 1 - results['distances'][0][i]
                    }
        
        # Sort by similarity
        sorted_results = sorted(all_results.values(), key=lambda x: x['similarity'], reverse=True)
        top_results = sorted_results[:request.num_results]
        
        # Format legal sections
        legal_sections = []
        for result in top_results:
            metadata = result['metadata']
            
            # Classify severity
            severity_level, reasoning, confidence = severity_classifier.classify(metadata)
            severity_summary = severity_classifier.get_severity_summary(severity_level)
            
            # Determine applicability
            applies_if = "Applies if: "
            if 'negligence' in keywords:
                applies_if += "proven negligent or rash"
            elif 'intention' in keywords:
                applies_if += "proven intentional"
            else:
                applies_if += "circumstances match this section"
            
            legal_sections.append(LegalSection(
                act=metadata.get('document_type', 'unknown').upper(),
                section=metadata.get('section_number', 'unknown'),
                title=metadata.get('section_title', ''),
                text=result['text'][:300] + "..." if len(result['text']) > 300 else result['text'],
                severity=severity_level.value,
                severity_icon=severity_summary['icon'],
                similarity=round(result['similarity'], 3),
                applies_if=applies_if
            ))
        
        # Determine overall severity
        overall_severity, severity_explanation = determine_overall_severity(
            [{'severity': s.severity} for s in legal_sections]
        )
        
        # Generate recommendations
        recommendations = generate_recommendations(overall_severity, keywords)
        
        # Identify key factors
        key_factors = identify_key_factors(situation, keywords)
        
        # Create summary
        situation_summary = f"Legal analysis for: {situation[:100]}..." if len(situation) > 100 else situation
        
        return SituationAnalysis(
            situation_summary=situation_summary,
            key_legal_terms=keywords,
            relevant_laws=legal_sections,
            overall_severity=overall_severity,
            severity_explanation=severity_explanation,
            key_factors=key_factors,
            recommendations=recommendations,
            disclaimer="⚠️ This is legal information only, NOT legal advice. Laws are complex and outcomes depend on specific facts, evidence, and court interpretation. Consult a qualified lawyer immediately for your specific situation. This analysis is based on Indian law and may not cover all applicable provisions.",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.get("/")
async def root():
    return {
        "message": "Enhanced Legal Analysis API",
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
