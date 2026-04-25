#!/usr/bin/env python3
"""
Comprehensive RAG Quality Testing

Tests retrieval accuracy, severity classification, and overall system quality.
"""

import json
import requests
from typing import Dict, List, Any
from datetime import datetime

# Test cases with expected results
TEST_CASES = [
    {
        "id": "accident_death_01",
        "situation": "I was driving in my lane when a person on scooty came from intersection and crashed into me. He is severely injured and may die.",
        "expected_sections": ["304A", "279", "337", "338"],  # IPC sections
        "expected_acts": ["IPC", "MOTOR_VEHICLES_ACT"],
        "expected_severity": ["YELLOW", "RED"],
        "expected_keywords": ["negligence", "rash driving", "causing death", "accident"],
        "min_relevance_score": 0.6
    },
    {
        "id": "theft_01",
        "situation": "Someone stole my phone from my pocket in a crowded market",
        "expected_sections": ["379", "380"],  # IPC theft sections
        "expected_acts": ["IPC"],
        "expected_severity": ["YELLOW", "GREEN"],
        "expected_keywords": ["theft", "stolen property", "punishment"],
        "min_relevance_score": 0.7
    },
    {
        "id": "assault_01",
        "situation": "My neighbor attacked me with a stick and broke my arm",
        "expected_sections": ["323", "324", "325"],  # IPC assault/hurt
        "expected_acts": ["IPC"],
        "expected_severity": ["YELLOW"],
        "expected_keywords": ["assault", "hurt", "grievous hurt", "weapon"],
        "min_relevance_score": 0.6
    },
    {
        "id": "defamation_01",
        "situation": "Someone posted false accusations about me on social media saying I am a thief",
        "expected_sections": ["499", "500"],  # IPC defamation
        "expected_acts": ["IPC"],
        "expected_severity": ["GREEN", "YELLOW"],
        "expected_keywords": ["defamation", "reputation", "false accusation"],
        "min_relevance_score": 0.5
    },
    {
        "id": "drunk_driving_01",
        "situation": "I was caught driving under influence of alcohol",
        "expected_sections": ["185", "184"],  # Motor Vehicles Act
        "expected_acts": ["MOTOR_VEHICLES_ACT", "IPC"],
        "expected_severity": ["GREEN", "YELLOW"],
        "expected_keywords": ["drunk", "alcohol", "driving", "intoxicated"],
        "min_relevance_score": 0.5
    },
    {
        "id": "murder_intentional_01",
        "situation": "I intentionally killed someone who was threatening my family",
        "expected_sections": ["302", "300", "100"],  # IPC murder, self-defense
        "expected_acts": ["IPC"],
        "expected_severity": ["RED"],
        "expected_keywords": ["murder", "intentional", "self defense", "death"],
        "min_relevance_score": 0.7
    },
    {
        "id": "property_damage_01",
        "situation": "My neighbor's tree fell on my car and damaged it",
        "expected_sections": ["425", "426"],  # IPC mischief
        "expected_acts": ["IPC", "CPC"],
        "expected_severity": ["GREEN", "YELLOW"],
        "expected_keywords": ["property damage", "mischief", "compensation"],
        "min_relevance_score": 0.4
    },
    {
        "id": "cheating_01",
        "situation": "Someone sold me a fake gold chain claiming it was real",
        "expected_sections": ["420", "415"],  # IPC cheating/fraud
        "expected_acts": ["IPC"],
        "expected_severity": ["YELLOW"],
        "expected_keywords": ["cheating", "fraud", "deception", "dishonest"],
        "min_relevance_score": 0.6
    }
]


def test_api_endpoint(api_url: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single case against the API."""
    try:
        response = requests.post(
            f"{api_url}/analyze",
            json={
                "situation": test_case["situation"],
                "num_results": 10
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def evaluate_results(test_case: Dict[str, Any], api_response: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate API response against expected results."""
    if not api_response.get("success"):
        return {
            "passed": False,
            "error": api_response.get("error"),
            "scores": {}
        }
    
    data = api_response["data"]
    relevant_laws = data.get("relevant_laws", [])
    
    # 1. Section Accuracy
    retrieved_sections = [law["section"] for law in relevant_laws]
    expected_sections = test_case["expected_sections"]
    
    section_matches = sum(1 for sec in expected_sections if any(sec in rs for rs in retrieved_sections))
    section_accuracy = section_matches / len(expected_sections) if expected_sections else 0
    
    # 2. Act Accuracy
    retrieved_acts = list(set([law["act"] for law in relevant_laws]))
    expected_acts = test_case["expected_acts"]
    
    act_matches = sum(1 for act in expected_acts if any(act in ra for ra in retrieved_acts))
    act_accuracy = act_matches / len(expected_acts) if expected_acts else 0
    
    # 3. Severity Accuracy
    overall_severity = data.get("overall_severity", "UNKNOWN")
    severity_correct = overall_severity in test_case["expected_severity"]
    
    # 4. Relevance Score (average similarity)
    if relevant_laws:
        avg_similarity = sum(law["similarity"] for law in relevant_laws) / len(relevant_laws)
        relevance_pass = avg_similarity >= test_case["min_relevance_score"]
    else:
        avg_similarity = 0
        relevance_pass = False
    
    # 5. Keyword Coverage
    retrieved_text = " ".join([law["text"].lower() for law in relevant_laws])
    keyword_matches = sum(1 for kw in test_case["expected_keywords"] if kw.lower() in retrieved_text)
    keyword_coverage = keyword_matches / len(test_case["expected_keywords"]) if test_case["expected_keywords"] else 0
    
    # Overall pass/fail
    passed = (
        section_accuracy >= 0.5 and  # At least 50% of expected sections
        act_accuracy >= 0.5 and      # At least 50% of expected acts
        severity_correct and          # Correct severity level
        relevance_pass               # Good relevance scores
    )
    
    return {
        "passed": passed,
        "scores": {
            "section_accuracy": round(section_accuracy, 2),
            "act_accuracy": round(act_accuracy, 2),
            "severity_correct": severity_correct,
            "avg_similarity": round(avg_similarity, 3),
            "keyword_coverage": round(keyword_coverage, 2),
            "relevance_pass": relevance_pass
        },
        "details": {
            "expected_sections": expected_sections,
            "retrieved_sections": retrieved_sections[:5],
            "expected_acts": expected_acts,
            "retrieved_acts": retrieved_acts,
            "expected_severity": test_case["expected_severity"],
            "actual_severity": overall_severity,
            "top_3_laws": [
                {
                    "act": law["act"],
                    "section": law["section"],
                    "similarity": law["similarity"]
                }
                for law in relevant_laws[:3]
            ]
        }
    }


def run_comprehensive_test(api_url: str = "http://localhost:8002"):
    """Run all test cases and generate report."""
    print("="*80)
    print("LEGAL RAG SYSTEM - COMPREHENSIVE QUALITY TEST")
    print("="*80)
    print(f"\nTesting API: {api_url}")
    print(f"Test Cases: {len(TEST_CASES)}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*80)
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n[{i}/{len(TEST_CASES)}] Testing: {test_case['id']}")
        print(f"Situation: {test_case['situation'][:80]}...")
        
        # Test API
        api_response = test_api_endpoint(api_url, test_case)
        
        # Evaluate
        evaluation = evaluate_results(test_case, api_response)
        
        # Store results
        results.append({
            "test_id": test_case["id"],
            "situation": test_case["situation"],
            "evaluation": evaluation
        })
        
        # Print result
        if evaluation["passed"]:
            print("✓ PASSED")
        else:
            print("✗ FAILED")
        
        if "scores" in evaluation:
            scores = evaluation["scores"]
            print(f"  Section Accuracy: {scores['section_accuracy']:.0%}")
            print(f"  Act Accuracy: {scores['act_accuracy']:.0%}")
            print(f"  Severity: {'✓' if scores['severity_correct'] else '✗'}")
            print(f"  Avg Similarity: {scores['avg_similarity']:.3f}")
            print(f"  Keyword Coverage: {scores['keyword_coverage']:.0%}")
    
    # Calculate overall metrics
    print("\n" + "="*80)
    print("OVERALL RESULTS")
    print("="*80)
    
    passed_tests = sum(1 for r in results if r["evaluation"]["passed"])
    total_tests = len(results)
    pass_rate = (passed_tests / total_tests) * 100
    
    # Average scores
    valid_results = [r for r in results if "scores" in r["evaluation"]]
    if valid_results:
        avg_section_acc = sum(r["evaluation"]["scores"]["section_accuracy"] for r in valid_results) / len(valid_results)
        avg_act_acc = sum(r["evaluation"]["scores"]["act_accuracy"] for r in valid_results) / len(valid_results)
        avg_similarity = sum(r["evaluation"]["scores"]["avg_similarity"] for r in valid_results) / len(valid_results)
        avg_keyword_cov = sum(r["evaluation"]["scores"]["keyword_coverage"] for r in valid_results) / len(valid_results)
        severity_correct_count = sum(1 for r in valid_results if r["evaluation"]["scores"]["severity_correct"])
        severity_accuracy = (severity_correct_count / len(valid_results)) * 100
    else:
        avg_section_acc = avg_act_acc = avg_similarity = avg_keyword_cov = severity_accuracy = 0
    
    print(f"\nTests Passed: {passed_tests}/{total_tests} ({pass_rate:.1f}%)")
    print(f"\nAverage Metrics:")
    print(f"  Section Accuracy: {avg_section_acc:.1%}")
    print(f"  Act Accuracy: {avg_act_acc:.1%}")
    print(f"  Severity Accuracy: {severity_accuracy:.1f}%")
    print(f"  Avg Similarity Score: {avg_similarity:.3f}")
    print(f"  Keyword Coverage: {avg_keyword_cov:.1%}")
    
    # Commercial readiness assessment
    print("\n" + "="*80)
    print("COMMERCIAL READINESS ASSESSMENT")
    print("="*80)
    
    readiness_score = (
        pass_rate * 0.4 +
        avg_section_acc * 100 * 0.2 +
        severity_accuracy * 0.2 +
        avg_similarity * 100 * 0.2
    )
    
    print(f"\nOverall Readiness Score: {readiness_score:.1f}/100")
    
    if readiness_score >= 80:
        status = "✓ READY FOR COMMERCIAL USE"
        recommendation = "System meets quality standards for production deployment."
    elif readiness_score >= 60:
        status = "⚠️ READY FOR BETA/TESTING"
        recommendation = "System is functional but needs improvements before full commercial use."
    else:
        status = "✗ NOT READY FOR COMMERCIAL USE"
        recommendation = "System requires significant improvements before deployment."
    
    print(f"Status: {status}")
    print(f"\nRecommendation: {recommendation}")
    
    # Specific issues
    print("\n" + "="*80)
    print("KEY ISSUES IDENTIFIED")
    print("="*80)
    
    failed_tests = [r for r in results if not r["evaluation"]["passed"]]
    if failed_tests:
        print(f"\nFailed Tests ({len(failed_tests)}):")
        for r in failed_tests:
            print(f"  • {r['test_id']}: {r['situation'][:60]}...")
            if "scores" in r["evaluation"]:
                scores = r["evaluation"]["scores"]
                if scores["section_accuracy"] < 0.5:
                    print(f"    - Poor section retrieval ({scores['section_accuracy']:.0%})")
                if not scores["severity_correct"]:
                    print(f"    - Incorrect severity classification")
                if not scores["relevance_pass"]:
                    print(f"    - Low relevance scores ({scores['avg_similarity']:.3f})")
    
    # Save report
    report = {
        "test_date": datetime.now().isoformat(),
        "api_url": api_url,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "pass_rate": pass_rate,
        "metrics": {
            "section_accuracy": avg_section_acc,
            "act_accuracy": avg_act_acc,
            "severity_accuracy": severity_accuracy,
            "avg_similarity": avg_similarity,
            "keyword_coverage": avg_keyword_cov
        },
        "readiness_score": readiness_score,
        "status": status,
        "detailed_results": results
    }
    
    with open("rag_quality_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: rag_quality_report.json")
    print("="*80)
    
    return report


if __name__ == "__main__":
    report = run_comprehensive_test()
