import json
import openai

# Define tools
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

# Define functions
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

def process_conversation(client, model, conversation_history, user_message, tools=tools):
    """Process a single user message and return the updated history and response"""
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
        final_content = f"API error: {e}"
        print(final_content)
        return conversation_history, final_content
    
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

    return conversation_history, final_content