import os
import json
from pathlib import Path
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

# 3. Define the conversation inputs
def read_conversation_inputs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read lines and strip whitespace, ignoring empty lines
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []

# Create responses directory if it doesn't exist
Path("responses").mkdir(exist_ok=True)

# Process each .txt file in the test_cases folder
test_cases_dir = "test_cases"
responses_dir = "responses"

for filename in os.listdir(test_cases_dir):
    if filename.endswith('.txt'):
        input_path = os.path.join(test_cases_dir, filename)
        output_filename = os.path.splitext(filename)[0] + '.json'
        output_path = os.path.join(responses_dir, output_filename)
        
        try:
            conversation_inputs = read_conversation_inputs(input_path)

            # 4. Initialize conversation history
            conversation_history = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            # Initialize dictionary to store conversation for JSON output
            conversation_output = {}

            print("=== Starting Conversation ===")
            print()

            # 5. Process each user input sequentially
            for i, user_message in enumerate(conversation_inputs, 1):
                print(f"--- Turn {i} ---")
                print(f"User: {user_message}")
                print()
                
                conversation_history, final_content = process_conversation(client, model, conversation_history, user_message, tools)

                # Store the turn in the conversation output
                conversation_output[f"turn_{i}"] = {
                    "user": user_message,
                    "ai": final_content or "No response generated"
                }
                
                print()

            print("=== Complete Conversation History ===")

            # 6. Print the complete conversation history
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(conversation_output, f, indent=2, ensure_ascii=False)
                print(f"Processed {filename} -> {output_filename}")
            except Exception as e:
                print(f"Error saving conversation to JSON: {str(e)}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

print("\nAll files processed successfully!")
