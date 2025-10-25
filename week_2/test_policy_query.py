#!/usr/bin/env python3
"""
Test script for policy query functionality
"""

from office_assistant import query_policy, load_policies_to_chroma

def test_policy_queries():
    """Test various policy queries"""
    
    print("=== Testing Policy Query Functionality ===\n")
    
    # Test queries
    test_questions = [
        "How many vacation days do I get per year?",
        "What is the sick leave policy?",
        "Can I work from home?",
        "What are the overtime rules?",
        "What is the dress code policy?",
        "How do I book a meeting room?",
        "What are the travel expense limits?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"Test {i+1}: {question}")
        print("-" * 50)
        try:
            result = query_policy(question)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    # Ensure policies are loaded
    print("Loading policies into ChromaDB...")
    load_policies_to_chroma()
    print("Policies loaded successfully!\n")
    
    # Run tests
    test_policy_queries()
