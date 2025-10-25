#!/usr/bin/env python3
"""
Simple test for policy functionality
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from office_assistant import query_policy, load_policies_to_chroma
    
    print("Testing policy query functionality...")
    
    # Load policies
    print("Loading policies...")
    load_policies_to_chroma()
    
    # Test a simple query
    print("\nTesting query: 'How many vacation days do I get?'")
    result = query_policy("How many vacation days do I get?")
    print("Result:")
    print(result)
    
    print("\nTest completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
