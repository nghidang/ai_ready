#!/usr/bin/env python3
"""
Test script for TTS functionality
"""
import os
import sys
from tts_module import text_to_speech, get_tts_instance

def test_tts_basic():
    """Test basic TTS functionality"""
    print("=== Testing Basic TTS Functionality ===")
    
    test_texts = [
        "Hello! I'm your office assistant.",
        "Your leave request has been submitted successfully.",
        "Meeting room A has been booked for tomorrow at 2 PM.",
        "Thank you for using the office assistant. Have a great day!"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text}")
        try:
            audio_path = text_to_speech(text, play_audio=True)
            if audio_path:
                print(f"✅ Success: Audio saved to {audio_path}")
            else:
                print("❌ Failed: No audio generated")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_tts_office_scenarios():
    """Test TTS with office assistant scenarios"""
    print("\n=== Testing Office Assistant Scenarios ===")
    
    scenarios = [
        {
            "name": "Leave Request",
            "text": "Your vacation request for December 15th has been submitted. You will receive confirmation from HR within 24 hours."
        },
        {
            "name": "Work from Home",
            "text": "Your work from home request for tomorrow has been approved. Please ensure you have access to all necessary systems."
        },
        {
            "name": "Meeting Room Booking",
            "text": "Conference room B has been booked for your team meeting on Friday from 10 AM to 11 AM."
        },
        {
            "name": "Policy Query",
            "text": "According to company policy, employees are entitled to 20 vacation days per year. Unused days can be carried over to the next year with manager approval."
        }
    ]
    
    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        print(f"Text: {scenario['text']}")
        try:
            audio_path = text_to_speech(scenario['text'], play_audio=True)
            if audio_path:
                print(f"✅ Success: Audio generated")
            else:
                print("❌ Failed: No audio generated")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_tts_performance():
    """Test TTS performance with different text lengths"""
    print("\n=== Testing TTS Performance ===")
    
    import time
    
    texts = [
        "Short response.",
        "This is a medium length response that should take a bit longer to process and generate audio for.",
        "This is a much longer response that contains multiple sentences and should demonstrate how the TTS system handles longer text inputs. It includes various punctuation marks and should provide a good test of the system's ability to process complex text structures."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\nPerformance Test {i} (Length: {len(text)} chars)")
        start_time = time.time()
        
        try:
            audio_path = text_to_speech(text, play_audio=False)  # Don't play to save time
            end_time = time.time()
            
            if audio_path:
                print(f"✅ Success: Generated in {end_time - start_time:.2f} seconds")
            else:
                print("❌ Failed: No audio generated")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Run all TTS tests"""
    print("🎵 TTS Testing Suite")
    print("=" * 50)
    
    # Check if TTS dependencies are available
    try:
        import torch
        import transformers
        print("✅ TTS dependencies found")
    except ImportError as e:
        print(f"❌ Missing TTS dependencies: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return
    
    # Run tests
    try:
        test_tts_basic()
        test_tts_office_scenarios()
        test_tts_performance()
        
        print("\n" + "=" * 50)
        print("🎉 TTS testing completed!")
        print("\nTo use TTS in the office assistant:")
        print("  python main.py --tts")
        print("\nTo disable TTS:")
        print("  python main.py --no-tts")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")

if __name__ == "__main__":
    main()
