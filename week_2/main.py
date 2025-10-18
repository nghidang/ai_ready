import os
import json
from pathlib import Path
from dotenv import load_dotenv
import openai

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

# 1. Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "request_day_off",
            "description": "Request a day off from work.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date for the day off in YYYY-MM-DD format",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for the day off",
                    },
                },
                "required": ["date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_wfh",
            "description": "Request to work from home.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date for working from home in YYYY-MM-DD format",
                    },
                },
                "required": ["date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_late_coming",
            "description": "Request permission to arrive late to work.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date for late arrival in YYYY-MM-DD format",
                    },
                    "time": {
                        "type": "string",
                        "description": "The expected arrival time in HH:MM format",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for arriving late",
                    },
                },
                "required": ["date", "time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_overtime",
            "description": "Request to work overtime.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date for overtime work in YYYY-MM-DD format",
                    },
                    "hours": {
                        "type": "number",
                        "description": "Number of overtime hours requested",
                    },
                },
                "required": ["date", "hours"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_assets",
            "description": "Request assets or equipment for work.",
            "parameters": {
                "type": "object",
                "properties": {
                    "assets": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Name of an asset (e.g., laptop, monitor)",
                        },
                        "description": "List of assets requested",
                    },
                },
                "required": ["assets"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_meeting_room",
            "description": "Book a meeting room for a specific time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date for the meeting in YYYY-MM-DD format",
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time of the meeting in HH:MM format",
                    },
                    "duration": {
                        "type": "number",
                        "description": "Duration of the meeting in hours",
                    },
                    "room_id": {
                        "type": "string",
                        "description": "Identifier for the meeting room",
                    },
                },
                "required": ["date", "start_time", "duration", "room_id"],
            },
        },
    },
]

# 2. Define the functions
def request_day_off(date, reason=None):
    reason_text = f" for {reason}" if reason else ""
    return f"Day off request for {date}{reason_text} has been submitted."

def request_wfh(date):
    return f"Work-from-home request for {date} has been submitted."

def request_late_coming(date, time, reason=None):
    reason_text = f" for {reason}" if reason else ""
    return f"Late arrival request for {date} at {time}{reason_text} has been submitted."

def request_overtime(date, hours):
    return f"Overtime request for {hours} hours on {date} has been submitted."

def request_assets(assets):
    return f"Asset request for {', '.join(assets)} has been submitted."

def book_meeting_room(date, start_time, duration, room_id):
    return f"Meeting room {room_id} booked on {date} from {start_time} for {duration} hours."

def execute_function(function_name, arguments):
    """Helper function to execute the appropriate function based on the tool call"""
    try:
        if function_name == "request_day_off":
            return request_day_off(arguments["date"], arguments.get("reason"))
        elif function_name == "request_wfh":
            return request_wfh(arguments["date"])
        elif function_name == "request_late_coming":
            return request_late_coming(arguments["date"], arguments["time"], arguments.get("reason"))
        elif function_name == "request_overtime":
            return request_overtime(arguments["date"], arguments["hours"])
        elif function_name == "request_assets":
            return request_assets(arguments["assets"])
        elif function_name == "book_meeting_room":
            return book_meeting_room(arguments["date"], arguments["start_time"], arguments["duration"], arguments["room_id"])
        else:
            return f"Unknown function: {function_name}"
    except KeyError as e:
        return f"Error: Missing required parameter {e}"
    except Exception as e:
        return f"Error executing function: {str(e)}"

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

conversation_inputs = read_conversation_inputs("test_cases/case_1.txt")

# 4. Initialize conversation history
conversation_history = [
    {
        "role": "system",
        "content": """
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
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    # First API call: Get model response with tools
    try:
        response = client.chat.completions.create(
            model=model,
            tools=tools,
            messages=conversation_history,
        )
    except openai.APIError as e:
        print(f"API error: {e}")
        continue
    
    # Process tool calls if any
    tool_calls_processed = False
    final_content = None
    
    for choice in response.choices:
        if choice.message.tool_calls:
            tool_calls_processed = True
            for tool_call in choice.message.tool_calls:
                # print("Tool call:")
                # print(json.dumps(tool_call.model_dump(), indent=2))

                function_name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}
                
                # Execute the function
                result = execute_function(function_name, arguments)
                
                # Add assistant message with tool call
                conversation_history.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": function_name,
                            "arguments": tool_call.function.arguments
                        }
                    }]
                })
                
                # Add tool response
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps({"result": result})
                })
        
        # If no tool calls, add the assistant message directly
        else:
            final_content = choice.message.content
            conversation_history.append({
                "role": "assistant",
                "content": choice.message.content
            })
    
    # Second API call: Get final response from model
    if tool_calls_processed:
        try:
            response = client.chat.completions.create(
                model=model,
                tools=tools,
                messages=conversation_history,
            )
            
            # Add final assistant response to history
            final_content = response.choices[0].message.content
            conversation_history.append({
                "role": "assistant",
                "content": final_content
            })
            
            print(f"AI: {final_content}")
            
        except openai.APIError as e:
            print(f"API error in final response: {e}")
            final_content = f"Error: {str(e)}"
    else:
        # If no tool calls were processed, the first response might already have content
        if response.choices[0].message.content and not final_content:
            final_content = response.choices[0].message.content
            print(f"AI: {final_content}")
    
    # Store the turn in the conversation output
    conversation_output[f"turn_{i}"] = {
        "user": user_message,
        "ai": final_content or "No response generated"
    }
    
    print()

print("=== Complete Conversation History ===")

# 6. Print the complete conversation history
try:
    with open("responses/case_1.json", "w", encoding="utf-8") as f:
        json.dump(conversation_output, f, indent=2, ensure_ascii=False)
    print("Conversation saved to conversation_output.json")
except Exception as e:
    print(f"Error saving conversation to JSON: {str(e)}")
