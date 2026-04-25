#!/usr/bin/env python3
"""
Seed Query Tests for Legal RAG System

Tests retrieval accuracy and answer quality using predefined Q&A pairs.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import pytest

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "src" / "rag"))

from rag_pipeline import LegalRAGPipeline


# Seed test queries with expected results
SEED_QUERIES = [
    {
        "id": "q001",
        "query": "What is the punishment for murder in India?",
        "expected_act": "ipc",
        "expected_section": "302",
        "expected_severity": "RED",
        "keywords": ["murder", "death", "life imprisonment", "302"]
    },
    {
        "id": "q002",
        "query": "Is theft a bailable offense?",
        "expected_act": "ipc",
        "expected_section": "379",
        "expected_severity": "YELLOW",
        "keywords": ["theft", "bailable", "379"]
    },
    {
        "id": "q003",
        "query": "What are the penalties for drunk driving?",
        "expected_act": "motor_vehicles_act",
        "expected_section": None,  # May vary
        "expected_severity": "GREEN",
        "keywords": ["drunk", "driving", "alcohol", "fine"]
    },
    {
        "id": "q004",
        "query": "Punishment for dowry harassment",
        "expected_act": "ipc",
        "expected_section": "498A",
        "expected_severity": "RED",
        "keywords": ["dowry", "harassment", "498"]
    },
    {
        "id": "q005",
        "query": "What is culpable homicide?",
        "expected_act": "ipc",
        "expected_section": "299",
        "expected_severity": "RED",
        "keywords": ["culpable", "homicide", "299"]
    },
    {
        "id": "q006",
        "query": "Penalty for cheating",
        "expected_act": "ipc",
        "expected_section": "420",
        "expected_severity": "YELLOW",
        "keywords": ["cheating", "fraud", "420"]
    },
    {
        "id": "q007",
        "query": "What is defamation under Indian law?",
        "expected_act": "ipc",
        "expected_section": "499",
        "expected_severity": "GREEN",
        "keywords": ["defamation", "reputation", "499"]
    },
    {
        "id": "q008",
        "query": "Punishment for rape",
        "expected_act": "ipc",
        "expected_section": "376",
        "expected_severity": "RED",
        "keywords": ["rape", "sexual", "376"]
    },
    {
        "id": "q009",
        "query": "What is the punishment for assault?",
        "expected_act": "ipc",
        "expected_section": "351",
        "expected_severity": "YELLOW",
        "keywords": ["assault", "force", "351"]
    },
    {
        "id": "q010",
        "query": "Is bribery a cognizable offense?",
        "expected_act": "ipc",
        "expected_section": None,
        "expected_severity": "RED",
        "keywords": ["bribery", "corruption", "cognizable"]
    }
]


class TestSeedQueries:
    """Test suite for seed queries."""
    
    @pytest.fixture(scope="class")
    def pipeline(self):
        """Initialize RAG pipeline once for all tests."""
        try:
            pipeline = LegalRAGPipeline()
            return pipeline
        except Exception as e:
            pytest.skip(f"Could not initialize pipeline: {e}")
    
    def test_retrieval_accuracy(self, pipeline):
        """Test if correct sections are retrieved."""
        results = []
        
        for seed in SEED_QUERIES:
            query = seed["query"]
            expected_act = seed["expected_act"]
            expected_section = seed["expected_section"]
            
            # Retrieve documents
            docs = pipeline.retrieve_relevant_chunks(query, k=5)
            
            # Check if expected section is in top-5
            found_act = False
            found_section = False
            
            for doc in docs:
                metadata = doc.metadata
                doc_type = metadata.get("document_type", "").lower()
                section_num = metadata.get("section_number", "").lower()
                
                if expected_act and expected_act in doc_type:
                    found_act = True
                
                if expected_section and expected_section.lower() in section_num:
                    found_section = True
            
            results.append({
                "id": seed["id"],
                "query": query,
                "found_act": found_act,
                "found_section": found_section if expected_section else None,
                "expected_act": expected_act,
                "expected_section": expected_section
            })
        
        # Calculate accuracy
        act_accuracy = sum(1 for r in results if r["found_act"]) / len(results)
        section_results = [r for r in results if r["found_section"] is not None]
        section_accuracy = sum(1 for r in section_results if r["found_section"]) / len(section_results) if section_results else 0
        
        print(f"\nRetrieval Accuracy:")
        print(f"  Act accuracy: {act_accuracy:.1%}")
        print(f"  Section accuracy: {section_accuracy:.1%}")
        
        # Assert minimum accuracy
        assert act_accuracy >= 0.8, f"Act retrieval accuracy {act_accuracy:.1%} below 80%"
        assert section_accuracy >= 0.7, f"Section retrieval accuracy {section_accuracy:.1%} below 70%"
    
    def test_severity_classification(self, pipeline):
        """Test if severity is correctly classified."""
        results = []
        
        for seed in SEED_QUERIES:
            query = seed["query"]
            expected_severity = seed["expected_severity"]
            
            # Get response
            response = pipeline.query(query)
            predicted_severity = response["severity"]["level"]
            
            is_correct = predicted_severity == expected_severity
            
            results.append({
                "id": seed["id"],
                "query": query,
                "expected": expected_severity,
                "predicted": predicted_severity,
                "correct": is_correct
            })
        
        # Calculate accuracy
        accuracy = sum(1 for r in results if r["correct"]) / len(results)
        
        print(f"\nSeverity Classification Accuracy: {accuracy:.1%}")
        
        # Print mismatches
        mismatches = [r for r in results if not r["correct"]]
        if mismatches:
            print("\nMismatches:")
            for m in mismatches:
                print(f"  {m['id']}: Expected {m['expected']}, got {m['predicted']}")
        
        # Assert minimum accuracy
        assert accuracy >= 0.7, f"Severity accuracy {accuracy:.1%} below 70%"
    
    def test_keyword_presence(self, pipeline):
        """Test if expected keywords appear in answers."""
        results = []
        
        for seed in SEED_QUERIES:
            query = seed["query"]
            expected_keywords = seed["keywords"]
            
            # Get response
            response = pipeline.query(query)
            answer = response["answer"].lower()
            
            # Check keyword presence
            found_keywords = [kw for kw in expected_keywords if kw.lower() in answer]
            keyword_score = len(found_keywords) / len(expected_keywords)
            
            results.append({
                "id": seed["id"],
                "query": query,
                "keyword_score": keyword_score,
                "found_keywords": found_keywords,
                "expected_keywords": expected_keywords
            })
        
        # Calculate average keyword score
        avg_score = sum(r["keyword_score"] for r in results) / len(results)
        
        print(f"\nKeyword Presence Score: {avg_score:.1%}")
        
        # Assert minimum score
        assert avg_score >= 0.5, f"Keyword presence {avg_score:.1%} below 50%"
    
    def test_citation_presence(self, pipeline):
        """Test if citations are provided."""
        for seed in SEED_QUERIES:
            query = seed["query"]
            
            # Get response
            response = pipeline.query(query)
            citations = response["citations"]
            
            # Assert citations exist
            assert len(citations) > 0, f"No citations for query: {query}"
            
            # Assert citation structure
            for citation in citations:
                assert "act" in citation
                assert "section" in citation
                assert "title" in citation
                assert "text_snippet" in citation
    
    def test_disclaimer_presence(self, pipeline):
        """Test if legal disclaimer is present."""
        for seed in SEED_QUERIES[:3]:  # Test first 3 queries
            query = seed["query"]
            
            # Get response
            response = pipeline.query(query)
            
            # Assert disclaimer exists
            assert "disclaimer" in response
            assert len(response["disclaimer"]) > 0
            assert "legal advice" in response["disclaimer"].lower()


def generate_test_report():
    """Generate a detailed test report."""
    print("\n" + "="*60)
    print("LEGAL RAG SYSTEM - SEED QUERY TEST REPORT")
    print("="*60)
    
    try:
        pipeline = LegalRAGPipeline()
    except Exception as e:
        print(f"Error: Could not initialize pipeline: {e}")
        return
    
    results = []
    
    for seed in SEED_QUERIES:
        print(f"\nTesting: {seed['id']} - {seed['query']}")
        
        try:
            response = pipeline.query(seed["query"])
            
            result = {
                "id": seed["id"],
                "query": seed["query"],
                "answer_length": len(response["answer"]),
                "num_citations": len(response["citations"]),
                "severity": response["severity"]["level"],
                "expected_severity": seed["expected_severity"],
                "severity_match": response["severity"]["level"] == seed["expected_severity"],
                "confidence": response["severity"]["confidence"]
            }
            
            results.append(result)
            
            print(f"  ✓ Answer length: {result['answer_length']} chars")
            print(f"  ✓ Citations: {result['num_citations']}")
            print(f"  ✓ Severity: {result['severity']} (expected: {result['expected_severity']})")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append({
                "id": seed["id"],
                "query": seed["query"],
                "error": str(e)
            })
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    successful = [r for r in results if "error" not in r]
    failed = [r for r in results if "error" in r]
    
    print(f"Total queries: {len(SEED_QUERIES)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if successful:
        severity_matches = sum(1 for r in successful if r["severity_match"])
        severity_accuracy = (severity_matches / len(successful)) * 100
        
        print(f"\nSeverity Accuracy: {severity_accuracy:.1f}%")
        print(f"Average citations: {sum(r['num_citations'] for r in successful) / len(successful):.1f}")
        print(f"Average answer length: {sum(r['answer_length'] for r in successful) / len(successful):.0f} chars")
    
    # Save report
    report_file = Path("tests/seed_query_report.json")
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    # Run with pytest or generate report
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        generate_test_report()
    else:
        pytest.main([__file__, "-v"])
