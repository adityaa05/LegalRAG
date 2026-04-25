#!/usr/bin/env python3
"""
Severity Classification Engine for Legal RAG System

Rule-based Red/Yellow/Green severity mapper for legal offenses.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum


class SeverityLevel(Enum):
    """Severity levels for legal offenses."""
    RED = "RED"  # High severity
    YELLOW = "YELLOW"  # Moderate severity
    GREEN = "GREEN"  # Low severity
    UNKNOWN = "UNKNOWN"  # Insufficient data


class SeverityClassifier:
    """Rule-based severity classifier for legal offenses."""
    
    def __init__(self, rules_file: Optional[str] = None):
        """
        Initialize severity classifier.
        
        Args:
            rules_file: Path to custom rules JSON file
        """
        self.rules_file = rules_file
        self.rules = self._load_rules()
        
        print("Severity Classifier initialized")
        print(f"Rules loaded: {len(self.rules)} categories")
    
    def _load_rules(self) -> Dict[str, Any]:
        """
        Load severity classification rules.
        
        Returns:
            Rules dictionary
        """
        # Default rules based on Indian law
        default_rules = {
            "RED": {
                "description": "High severity - Non-bailable, serious offenses",
                "conditions": {
                    "bailable": ["No", "no", False],
                    "penalty_keywords": ["death", "life imprisonment", "life"],
                    "min_years": 10,
                    "offense_types": ["homicide", "sexual", "terrorism", "treason"]
                }
            },
            "YELLOW": {
                "description": "Moderate severity - Bailable but serious",
                "conditions": {
                    "min_years": 3,
                    "max_years": 10,
                    "offense_types": ["violence", "property", "fraud", "corruption"]
                }
            },
            "GREEN": {
                "description": "Low severity - Minor offenses",
                "conditions": {
                    "max_years": 3,
                    "penalty_keywords": ["fine only", "warning"],
                    "offense_types": ["traffic", "regulatory", "petty"]
                }
            }
        }
        
        # Load custom rules if provided
        if self.rules_file and Path(self.rules_file).exists():
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                custom_rules = json.load(f)
                print(f"Loaded custom rules from: {self.rules_file}")
                return custom_rules
        
        return default_rules
    
    def classify(
        self,
        metadata: Dict[str, Any],
        text: Optional[str] = None
    ) -> Tuple[SeverityLevel, str, float]:
        """
        Classify severity based on metadata and text.
        
        Args:
            metadata: Chunk metadata with legal attributes
            text: Optional text content for additional analysis
            
        Returns:
            Tuple of (severity_level, reasoning, confidence)
        """
        # Extract relevant fields
        bailable = metadata.get('bailable')
        cognizable = metadata.get('cognizable')
        max_penalty_years = metadata.get('maximum_punishment_years')
        offense_type = metadata.get('offense_type', '').lower()
        punishment_severity = metadata.get('punishment_severity', '').lower()
        involves_imprisonment = metadata.get('involves_imprisonment', False)
        involves_fine = metadata.get('involves_fine', False)
        
        # Convert string booleans to actual booleans
        if isinstance(bailable, str):
            bailable = bailable.lower() in ['yes', 'true']
        if isinstance(involves_imprisonment, str):
            involves_imprisonment = involves_imprisonment.lower() in ['true', 'yes']
        if isinstance(involves_fine, str):
            involves_fine = involves_fine.lower() in ['true', 'yes']
        
        # Combine text sources for keyword analysis
        combined_text = ""
        if text:
            combined_text += text.lower() + " "
        combined_text += metadata.get('section_title', '').lower() + " "
        combined_text += punishment_severity
        
        # Rule-based classification
        reasoning_parts = []
        confidence = 0.0
        
        # RED: High severity checks
        # Check death/life first (highest priority)
        if any(keyword in combined_text for keyword in ['death', 'capital punishment']):
            return (
                SeverityLevel.RED,
                "Capital punishment (death penalty)",
                1.0
            )
        
        if max_penalty_years and max_penalty_years >= 999:  # Life imprisonment marker
            return (
                SeverityLevel.RED,
                "Life imprisonment or death penalty",
                0.95
            )
        
        if any(keyword in combined_text for keyword in ['life imprisonment', 'imprisonment for life']):
            return (
                SeverityLevel.RED,
                "Life imprisonment",
                0.95
            )
        
        # Non-bailable + high penalty = RED
        if (bailable is False or bailable == "No") and max_penalty_years and max_penalty_years >= 7:
            return (
                SeverityLevel.RED,
                f"Non-bailable with {max_penalty_years} years imprisonment",
                0.9
            )
        
        if max_penalty_years and max_penalty_years >= 10:
            return (
                SeverityLevel.RED,
                f"Maximum penalty: {max_penalty_years} years (≥10 years)",
                0.9
            )
        
        if offense_type in ['homicide', 'sexual', 'murder', 'rape']:
            return (
                SeverityLevel.RED,
                f"Serious offense type: {offense_type}",
                0.9
            )
        
        # YELLOW: Moderate severity checks
        # Bailable but serious (1-7 years)
        if max_penalty_years and 1 <= max_penalty_years < 10:
            if bailable is True or bailable == "Yes":
                return (
                    SeverityLevel.YELLOW,
                    f"Bailable offense with {max_penalty_years} years imprisonment",
                    0.85
                )
            # Non-bailable with lower penalty
            elif bailable is False and max_penalty_years < 7:
                return (
                    SeverityLevel.YELLOW,
                    f"Non-bailable with {max_penalty_years} years imprisonment",
                    0.85
                )
        
        if offense_type in ['violence', 'property', 'fraud', 'corruption', 'assault', 'negligence']:
            if involves_imprisonment:
                return (
                    SeverityLevel.YELLOW,
                    f"Moderate offense with imprisonment: {offense_type}",
                    0.8
                )
        
        if punishment_severity in ['high', 'medium']:
            return (
                SeverityLevel.YELLOW,
                f"Punishment severity: {punishment_severity}",
                0.75
            )
        
        # GREEN: Low severity checks
        # Defamation and other minor offenses (≤2 years, bailable, non-cognizable)
        if offense_type in ['defamation']:
            return (
                SeverityLevel.GREEN,
                f"Minor offense: {offense_type} (typically bailable, non-cognizable)",
                0.85
            )
        
        if max_penalty_years and max_penalty_years <= 2:
            if bailable is True or bailable == "Yes":
                return (
                    SeverityLevel.GREEN,
                    f"Low penalty: {max_penalty_years} years (≤2 years, bailable)",
                    0.85
                )
        
        if involves_fine and not involves_imprisonment:
            return (
                SeverityLevel.GREEN,
                "Fine only, no imprisonment",
                0.9
            )
        
        if offense_type in ['traffic', 'regulatory', 'petty']:
            return (
                SeverityLevel.GREEN,
                f"Minor offense type: {offense_type}",
                0.8
            )
        
        if offense_type in ['traffic', 'regulatory', 'petty', 'defamation']:
            return (
                SeverityLevel.GREEN,
                f"Minor offense type: {offense_type}",
                0.8
            )
        
        if punishment_severity == 'low':
            return (
                SeverityLevel.GREEN,
                "Low punishment severity",
                0.75
            )
        
        # UNKNOWN: Insufficient data
        return (
            SeverityLevel.UNKNOWN,
            "Insufficient data for classification",
            0.0
        )
    
    def classify_batch(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Classify severity for a batch of chunks.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Chunks with added severity classification
        """
        print(f"Classifying severity for {len(chunks)} chunks...")
        
        for chunk in chunks:
            severity, reasoning, confidence = self.classify(
                metadata=chunk,
                text=chunk.get('text')
            )
            
            chunk['severity_level'] = severity.value
            chunk['severity_reasoning'] = reasoning
            chunk['severity_confidence'] = confidence
        
        # Calculate distribution
        distribution = {}
        for chunk in chunks:
            level = chunk['severity_level']
            distribution[level] = distribution.get(level, 0) + 1
        
        print("Severity distribution:")
        for level, count in sorted(distribution.items()):
            percentage = (count / len(chunks)) * 100
            print(f"  {level}: {count} ({percentage:.1f}%)")
        
        return chunks
    
    def get_severity_summary(self, severity_level: SeverityLevel) -> Dict[str, str]:
        """
        Get human-readable summary for a severity level.
        
        Args:
            severity_level: Severity level enum
            
        Returns:
            Summary dictionary with color, label, and description
        """
        summaries = {
            SeverityLevel.RED: {
                "color": "#DC2626",  # Red
                "label": "High Severity",
                "description": "Non-bailable offense or serious crime with severe penalties (10+ years, life imprisonment, or death)",
                "icon": "🔴",
                "action": "Consult a criminal defense lawyer immediately"
            },
            SeverityLevel.YELLOW: {
                "color": "#F59E0B",  # Yellow/Orange
                "label": "Moderate Severity",
                "description": "Bailable but serious offense with moderate penalties (3-10 years imprisonment)",
                "icon": "🟡",
                "action": "Legal consultation recommended"
            },
            SeverityLevel.GREEN: {
                "color": "#10B981",  # Green
                "label": "Low Severity",
                "description": "Minor offense with low penalties (<3 years or fine only)",
                "icon": "🟢",
                "action": "May be resolved with legal guidance"
            },
            SeverityLevel.UNKNOWN: {
                "color": "#6B7280",  # Gray
                "label": "Unknown",
                "description": "Insufficient information to determine severity",
                "icon": "⚪",
                "action": "Review source documents for details"
            }
        }
        
        return summaries.get(severity_level, summaries[SeverityLevel.UNKNOWN])
    
    def validate_classifications(
        self,
        test_cases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate classifier against test cases.
        
        Args:
            test_cases: List of test cases with expected severity
            
        Returns:
            Validation statistics
        """
        print(f"\nValidating classifier with {len(test_cases)} test cases...")
        
        correct = 0
        total = len(test_cases)
        results = []
        
        for test_case in test_cases:
            expected = test_case.get('expected_severity')
            metadata = test_case.get('metadata', {})
            text = test_case.get('text', '')
            
            predicted, reasoning, confidence = self.classify(metadata, text)
            
            is_correct = predicted.value == expected
            if is_correct:
                correct += 1
            
            results.append({
                "test_id": test_case.get('id', 'unknown'),
                "expected": expected,
                "predicted": predicted.value,
                "correct": is_correct,
                "confidence": confidence,
                "reasoning": reasoning
            })
        
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        stats = {
            "total_cases": total,
            "correct": correct,
            "incorrect": total - correct,
            "accuracy": round(accuracy, 2),
            "results": results
        }
        
        print(f"Accuracy: {accuracy:.1f}% ({correct}/{total})")
        
        return stats


def main():
    """Main execution function for testing."""
    classifier = SeverityClassifier()
    
    # Test cases
    test_cases = [
        {
            "id": "test_1",
            "metadata": {
                "section_number": "302",
                "section_title": "Punishment for murder",
                "offense_type": "homicide",
                "bailable": False,
                "maximum_punishment_years": 0,
                "punishment_severity": "severe"
            },
            "text": "Whoever commits murder shall be punished with death or life imprisonment",
            "expected_severity": "RED"
        },
        {
            "id": "test_2",
            "metadata": {
                "section_number": "379",
                "section_title": "Punishment for theft",
                "offense_type": "property",
                "bailable": True,
                "maximum_punishment_years": 3,
                "involves_imprisonment": True
            },
            "text": "Imprisonment up to 3 years or fine or both",
            "expected_severity": "YELLOW"
        },
        {
            "id": "test_3",
            "metadata": {
                "section_number": "177",
                "section_title": "Traffic violation",
                "offense_type": "traffic",
                "bailable": True,
                "maximum_punishment_years": 0,
                "involves_fine": True,
                "involves_imprisonment": False
            },
            "text": "Fine up to Rs. 5000",
            "expected_severity": "GREEN"
        }
    ]
    
    # Validate
    stats = classifier.validate_classifications(test_cases)
    
    print("\n" + "="*60)
    print("SEVERITY CLASSIFICATION TEST")
    print("="*60)
    
    for result in stats['results']:
        status = "✓" if result['correct'] else "✗"
        print(f"\n{status} Test {result['test_id']}")
        print(f"  Expected: {result['expected']}")
        print(f"  Predicted: {result['predicted']} (confidence: {result['confidence']:.2f})")
        print(f"  Reasoning: {result['reasoning']}")
    
    print(f"\nOverall Accuracy: {stats['accuracy']}%")


if __name__ == "__main__":
    main()
