#!/usr/bin/env python3
"""
Demo script showing how to use the office assistant with policy queries
"""

import os
from dotenv import load_dotenv
import openai
from office_assistant import SYSTEM_PROMPT, tools, process_conversation

# Load environment variables from .env file
load_dotenv()

# Read configuration from environment variables
model = os.getenv('MODEL')
base_url = os.getenv('OPENAI_BASE_URL')
api_key = os.getenv('OPENAI_API_KEY')

if not model:
    raise ValueError("MODEL is not set in .env file")
if not base_url:
    raise ValueError("OPENAI_BASE_URL is not set in .env file")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")

client = openai.OpenAI(
    base_url=base_url,
    api_key=api_key
)

def demo_policy_queries():
    """Demonstrate policy query functionality"""
    
    # Sample policy questions
    demo_questions = [
        "How many vacation days am I entitled to per year?",
        "What is the policy for working from home?",
        "What are the overtime rules and compensation?",
        "What is the dress code policy?",
        "How do I request sick leave?",
        "What are the travel expense limits?"
    ]
    
    print("=== Office Assistant Policy Query Demo ===\n")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"Demo {i}: {question}")
        print("-" * 60)
        
        # Initialize conversation history
        conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        
        try:
            # Process the question
            conversation_history, response = process_conversation(
                client, model, conversation_history, question, tools
            )
            print(f"Assistant: {response or 'No response generated'}\n")
        except Exception as e:
            print(f"Error processing question: {str(e)}\n")
        
        print("=" * 60 + "\n")

if __name__ == "__main__":
    demo_policy_queries()
