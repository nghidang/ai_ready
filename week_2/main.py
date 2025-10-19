import os
from dotenv import load_dotenv
import openai
from office_assistant import tools, process_conversation

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

# System prompt for the assistant
SYSTEM_PROMPT = """
You are an internal office assistant that helps employees handle internal requests. Your only responsibilities include:
    1. Submitting leave requests (vacation, sick leave, etc.)
    2. Requesting to work remotely
    3. Requesting to arrive late or leave early
    4. Requesting overtime approval
    5. Requesting office equipment or supplies
    6. Booking meeting rooms
When responding, always:
    - Respond with the result from the appropriate tool.
    - Be polite, concise, and professional.
    - Confirm all key details (date, time, reason, duration, etc.).
    - Provide a clear summary of the request and next steps (e.g., who will approve it, when confirmation will be sent).
    - Use a friendly but business-appropriate tone.
"""

def main():
    # Initialize conversation history
    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    print("=== Office Assistant ===")
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
            conversation_history, final_content = process_conversation(client, model, conversation_history, user_message, tools)
            print(f"Assistant: {final_content or 'No response generated'}\n")
        except Exception as e:
            print(f"Error processing request: {str(e)}\n")

        print("====================================\n")

if __name__ == "__main__":
    main()