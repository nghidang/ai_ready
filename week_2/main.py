import os
import argparse
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

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Office Assistant with TTS support")
    parser.add_argument("--tts", action="store_true", help="Enable text-to-speech audio responses")
    parser.add_argument("--no-tts", action="store_true", help="Disable text-to-speech audio responses")
    args = parser.parse_args()
    
    # Determine TTS setting
    enable_tts = args.tts or (not args.no_tts)  # Default to enabled unless explicitly disabled
    
    # Initialize conversation history
    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    print("=== Office Assistant ===")
    if enable_tts:
        print("🔊 Audio responses available (request with keywords like 'audio', 'voice', 'speak')")
    else:
        print("🔇 Audio responses disabled")
    
    print("I can help you with:")
    print("- Leave requests (vacation, sick leave)")
    print("- Work from home requests")
    print("- Late arrival/early departure requests")
    print("- Overtime approval requests")
    print("- Office equipment requests")
    print("- Meeting room bookings")
    print("- Company policy questions")
    print("\n💡 Tip: Add words like 'audio', 'voice', or 'speak' to your request for audio responses")
    print("Type your request (or 'exit' to quit):")
    
    while True:
        # Read user input from CLI
        user_message = input("You: ").strip()
        
        if user_message.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not user_message:
            print("Please enter a valid request.")
            continue
        
        print(f"\nProcessing request...\n")
        
        # Process the user message
        try:
            conversation_history, final_content = process_conversation(
                client, model, conversation_history, user_message, tools, enable_tts
            )
            print(f"Assistant: {final_content or 'No response generated'}\n")
        except Exception as e:
            print(f"Error processing request: {str(e)}\n")

        print("====================================\n")

if __name__ == "__main__":
    main()