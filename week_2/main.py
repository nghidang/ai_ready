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

def main():
    # Initialize conversation history
    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    print("""
=== Office Assistant ===
I can help you with:
- Leave requests (vacation, sick leave)
- Work from home requests
- Late arrival/early departure requests
- Overtime approval requests
- Office equipment requests
- Meeting room bookings
- Company policy questions

💡 Tip: Add words like 'audio', 'voice', or 'speak' to your request for audio responses
Type your request (or 'exit' to quit):
""")
    
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
            conversation_history, final_content = process_conversation(client, model, conversation_history, user_message, tools)
            print(f"Assistant: {final_content or 'No response generated'}\n")
        except Exception as e:
            print(f"Error processing request: {str(e)}\n")

        print("====================================\n")

if __name__ == "__main__":
    main()