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

# Create a running input list we will add to over time
input_list = [
    {"role": "user", "content": "I want to request a day off on 2025-11-01 for a family event."},
    {"role": "user", "content": "I want to request a day off."},
    {"role": "user", "content": "2025-11-01."},
    {"role": "user", "content": "A family event."},
    # You can test other inputs, e.g.:
    # {"role": "user", "content": "I want to work from home on 2025-11-02."}
    # {"role": "user", "content": "I need to come late on 2025-11-03 at 10:00 due to a doctor's appointment."}
    # {"role": "user", "content": "I want to work 3 hours overtime on 2025-11-04."}
    # {"role": "user", "content": "I need a laptop and a monitor for work."}
    # {"role": "user", "content": "Book a meeting room on 2025-11-05 from 14:00 for 2 hours in room A1."}
]

# 3. Prompt the model with tools defined
try:
    response = client.chat.completions.create(
        model=model,
        tools=tools,
        messages=input_list,
    )
except openai.APIError as e:
    print(f"API error: {e}")
    raise

# Process the response and append to input_list
for choice in response.choices:
    if choice.message.tool_calls:
        for tool_call in choice.message.tool_calls:
            print("Tool call:")
            print(json.dumps(tool_call.model_dump(), indent=2))

            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # 4. Execute the appropriate function based on the tool call
            result = execute_function(function_name, arguments)

            # 5. Append the tool call and its result to input_list
            input_list.append({
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
            input_list.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps({"result": result})
            })

print("Final input:")
print(json.dumps(input_list, indent=2))

# 6. Prompt the model again with the updated input_list
# Using a system message for instructions
# input_list_with_instructions = [
#     {
#         "role": "system",
#         "content": "Respond only with the result generated by a tool."
#     }
# ] + input_list

try:
    response = client.chat.completions.create(
        model=model,
        tools=tools,
        messages=input_list,
    )
except openai.APIError as e:
    print(f"API error: {e}")
    raise

# 7. Print the final output
print("Final output:")
print(response.choices[0].message.content)