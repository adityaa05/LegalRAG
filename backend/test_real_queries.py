#!/usr/bin/env python3
"""
Test Real-Life Legal Queries
Interactive testing with actual user scenarios
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:8002/analyze"

def test_query(situation, description=""):
    """Test a single query and display results."""
    print("\n" + "="*80)
    if description:
        print(f"TEST: {description}")
    print("="*80)
    print(f"Query: {situation[:100]}...")
    print("-"*80)
    
    try:
        response = requests.post(
            API_URL,
            json={"situation": situation},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Display results
            print(f"\n🚨 OVERALL SEVERITY: {result['overall_severity']}")
            print(f"\n📚 RELEVANT LAWS ({len(result['relevant_laws'])} found):")
            
            for i, law in enumerate(result['relevant_laws'][:5], 1):
                print(f"\n{i}. Section {law.get('section', 'N/A')}: {law.get('title', 'N/A')}")
                print(f"   Act: {law.get('act', 'N/A')}")
                print(f"   Severity: {law.get('severity', 'N/A')}")
                print(f"   Bailable: {law.get('bailable', 'N/A')}")
                print(f"   Cognizable: {law.get('cognizable', 'N/A')}")
                print(f"   Max Punishment: {law.get('max_punishment', 'N/A')}")
                print(f"   Text: {law.get('text', 'N/A')[:150]}...")
            
            print(f"\n🔑 KEY FACTORS:")
            for factor in result['key_factors'][:5]:
                print(f"   • {factor}")
            
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in result['recommendations'][:5]:
                print(f"   • {rec}")
            
            print(f"\n✓ Response time: {response.elapsed.total_seconds():.2f}s")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: API not running!")
        print("Start the API first: ./start_enhanced_api.sh")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Real-life test scenarios
test_scenarios = [
    {
        "description": "Domestic Violence",
        "query": "My husband beats me regularly and threatens to kill me if I tell anyone. He also doesn't let me go out of the house. What legal action can I take?"
    },
    {
        "description": "Road Accident",
        "query": "I was driving carefully when suddenly a bike came from the wrong side and hit my car. The rider got injured badly. Am I responsible? What will happen to me?"
    },
    {
        "description": "Online Fraud",
        "query": "Someone created a fake profile using my photos and is asking my friends for money. They are also posting bad things about me. What can I do legally?"
    },
    {
        "description": "Workplace Harassment",
        "query": "My boss keeps making inappropriate comments about my appearance and touches me without consent. I'm scared to complain. What are my legal options?"
    },
    {
        "description": "Property Dispute",
        "query": "My neighbor built a wall on my property without permission. When I objected, he threatened to harm me. What legal steps should I take?"
    },
    {
        "description": "Theft at Home",
        "query": "Someone broke into my house at night while we were sleeping and stole jewelry worth 5 lakhs. What charges can be filed?"
    },
    {
        "description": "Dowry Harassment",
        "query": "My in-laws are demanding more dowry and torturing me mentally. They threaten to throw me out. What legal protection do I have?"
    },
    {
        "description": "Cyber Stalking",
        "query": "An unknown person keeps sending me vulgar messages and photos on WhatsApp. They also follow me and take my pictures. How do I stop this legally?"
    },
    {
        "description": "Bribery",
        "query": "A police officer is asking for 50,000 rupees to not file a false case against me. What should I do?"
    },
    {
        "description": "Child Abuse",
        "query": "I suspect my neighbor is physically abusing their child. I can hear screaming and crying daily. What is my legal duty?"
    }
]

def interactive_mode():
    """Interactive query mode."""
    print("\n" + "="*80)
    print("INTERACTIVE MODE - Enter your own queries")
    print("="*80)
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("\n📝 Enter your legal query: ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            break
        
        if not query:
            continue
        
        test_query(query, "Your Query")

def main():
    """Main test function."""
    print("="*80)
    print("LEGAL RAG SYSTEM - REAL-LIFE QUERY TESTING")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API: {API_URL}")
    print(f"Test Scenarios: {len(test_scenarios)}")
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8002/health", timeout=2)
        print(f"✓ API Status: {response.json()['status']}")
    except:
        print("✗ API not running! Start it with: ./start_enhanced_api.sh")
        return
    
    print("\n" + "="*80)
    print("CHOOSE TEST MODE:")
    print("="*80)
    print("1. Run all 10 pre-defined scenarios")
    print("2. Interactive mode (enter your own queries)")
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        print("\n" + "="*80)
        print("RUNNING PRE-DEFINED SCENARIOS")
        print("="*80)
        
        passed = 0
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n[{i}/{len(test_scenarios)}]")
            if test_query(scenario['query'], scenario['description']):
                passed += 1
            input("\nPress ENTER for next test...")
        
        print("\n" + "="*80)
        print(f"RESULTS: {passed}/{len(test_scenarios)} queries processed successfully")
        print("="*80)
    
    if choice in ['2', '3']:
        interactive_mode()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
