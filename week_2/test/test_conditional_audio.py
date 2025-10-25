#!/usr/bin/env python3
"""
Test script for conditional audio functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from office_assistant import detect_audio_request

def test_audio_detection():
    """Test the audio request detection function"""
    print("=== Testing Audio Request Detection ===")
    
    test_cases = [
        # Should trigger audio
        ("I want to request a day off with audio", True),
        ("Can you speak the policy about vacation days?", True),
        ("Tell me about work from home policy in voice", True),
        ("I need to book a meeting room, please say it", True),
        ("What's the overtime policy? Audio please", True),
        ("Read aloud the company policies", True),
        ("Voice response for my leave request", True),
        ("Speak the meeting room availability", True),
        ("Audio response for equipment request", True),
        ("Say the work schedule", True),
        
        # Should NOT trigger audio
        ("I want to request a day off", False),
        ("What's the vacation policy?", False),
        ("Book a meeting room for tomorrow", False),
        ("I need office equipment", False),
        ("What are the work hours?", False),
        ("Tell me about sick leave", False),
        ("I want to work from home", False),
        ("Request overtime for Friday", False),
        ("What's the dress code?", False),
        ("How do I submit expenses?", False),
    ]
    
    print("Testing audio request detection...")
    print("-" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for i, (message, expected) in enumerate(test_cases, 1):
        result = detect_audio_request(message)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        print(f"Test {i:2d}: {status}")
        print(f"  Input: '{message}'")
        print(f"  Expected: {expected}, Got: {result}")
        print()
        
        if result == expected:
            passed += 1
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")
    
    return passed == total

def test_example_usage():
    """Show example usage of the conditional audio feature"""
    print("\n=== Example Usage ===")
    print("The office assistant now supports conditional audio responses.")
    print("Audio will only be generated when you explicitly request it.")
    print()
    print("Examples of requests that will trigger audio:")
    print("  • 'I want to request a day off with audio'")
    print("  • 'Can you speak the vacation policy?'")
    print("  • 'Tell me about work from home in voice'")
    print("  • 'Read aloud the meeting room booking process'")
    print()
    print("Examples of requests that will NOT trigger audio:")
    print("  • 'I want to request a day off'")
    print("  • 'What's the vacation policy?'")
    print("  • 'Book a meeting room for tomorrow'")
    print("  • 'I need office equipment'")
    print()
    print("Keywords that trigger audio:")
    print("  • audio, voice, speak, say, tell me, read aloud")
    print("  • speak it, voice response, audio response, sound")
    print("  • hear, listen, vocal, spoken, narrate")
    print("  • with audio, in audio, as audio, audio please")
    print("  • voice please, speak please, say it, read it")

def main():
    """Run all conditional audio tests"""
    print("🎵 Conditional Audio Testing Suite")
    print("=" * 50)
    
    # Test audio detection
    success = test_audio_detection()
    
    # Show example usage
    test_example_usage()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Conditional audio functionality is working correctly!")
        print("\nTo test in the office assistant:")
        print("  python main.py")
        print("\nThen try requests like:")
        print("  'I want to request a day off with audio'")
        print("  'Can you speak the vacation policy?'")
    else:
        print("⚠️  Some tests failed. Please check the audio detection logic.")
    
    return success

if __name__ == "__main__":
    main()
