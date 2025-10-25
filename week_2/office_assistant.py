import json
import openai
import os
from dotenv import load_dotenv
import tiktoken
import chromadb
from sentence_transformers import SentenceTransformer
from tts_module import text_to_speech

# Load environment variables from .env file
load_dotenv()

# Fix tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

MAX_TOKENS = int(os.getenv('MAX_TOKENS', 200))
if not MAX_TOKENS:
    raise ValueError("MAX_TOKENS is not set in .env file")

# Initialize ChromaDB and embedding model
def initialize_chroma_db():
    """Initialize ChromaDB client and embedding model"""
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path="./chroma_db")
        
        # Initialize embedding model
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        collection = client.get_or_create_collection(
            name="policies",
            metadata={"hnsw:space": "cosine"}
        )
        
        return client, collection, embedding_model
    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        return None, None, None

# Initialize ChromaDB components
chroma_client, policies_collection, embedding_model = initialize_chroma_db()

def load_policies_to_chroma():
    """Load policies from JSON file into ChromaDB"""
    if not policies_collection or not embedding_model:
        return False
    
    try:
        # Load policies from JSON file
        with open('example_policies.json', 'r') as f:
            policies = json.load(f)
        
        # Check if policies are already loaded
        if policies_collection.count() > 0:
            print("Policies already loaded in ChromaDB")
            return True
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for policy in policies:
            documents.append(policy['text'])
            metadatas.append(policy['metadata'])
            ids.append(policy['id'])
        
        # Add to ChromaDB
        policies_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Loaded {len(policies)} policies into ChromaDB")
        return True
        
    except Exception as e:
        print(f"Error loading policies: {e}")
        return False

def query_policies(question, n_results=3):
    """Query policies using semantic search"""
    if not policies_collection or not embedding_model:
        return "Policy database not available. Please check ChromaDB setup."
    
    try:
        # Generate embedding for the question
        query_embedding = embedding_model.encode(question).tolist()
        
        # Search in ChromaDB
        results = policies_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "No relevant policies found."
        
        # Format results
        formatted_results = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            formatted_results.append({
                'text': doc,
                'metadata': metadata,
                'relevance_score': 1 - distance  # Convert distance to similarity
            })
        
        return formatted_results
        
    except Exception as e:
        return f"Error querying policies: {str(e)}"

# Load policies on startup
load_policies_to_chroma()

# System prompt for the assistant
SYSTEM_PROMPT = """
You are an internal office assistant that helps employees handle internal requests. Your responsibilities include:
    1. Submitting leave requests (vacation, sick leave, etc.)
    2. Requesting to work remotely
    3. Requesting to arrive late or leave early
    4. Requesting overtime approval
    5. Requesting office equipment or supplies
    6. Booking meeting rooms
    7. Answering questions about company policies
When responding, always:
    - Respond shortly and concisely with the result from the appropriate tool.
    - Be polite, concise, and professional.
    - Confirm all key details (date, time, reason, duration, etc.).
    - Provide a clear summary of the request and next steps (e.g., who will approve it, when confirmation will be sent).
    - Use a friendly but business-appropriate tone.
    - When answering policy questions, provide accurate information based on the company policies and cite relevant policy details.
"""

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
    {
        "type": "function",
        "function": {
            "name": "query_policy",
            "description": "Answer questions about company policies by searching the policy database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The policy question to search for",
                    },
                },
                "required": ["question"],
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

def query_policy(question):
    """Query company policies and return relevant information"""
    try:
        results = query_policies(question)
        
        if isinstance(results, str):  # Error message
            return results
        
        if not results:
            return "No relevant policies found for your question."
        
        # Format the response
        response = "Based on company policies:\n\n"
        for i, result in enumerate(results, 1):
            response += f"{i}. **{result['metadata']['category']}** (Relevance: {result['relevance_score']:.2f})\n"
            response += f"   {result['text']}\n"
            if 'effective_date' in result['metadata']:
                response += f"   *Effective: {result['metadata']['effective_date']}*\n"
            response += "\n"
        
        return response
        
    except Exception as e:
        return f"Error querying policies: {str(e)}"

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
        elif function_name == "query_policy":
            return query_policy(arguments["question"])
        else:
            return f"Unknown function: {function_name}"
    except KeyError as e:
        return f"Error: Missing required parameter {e}"
    except Exception as e:
        return f"Error executing function: {str(e)}"

def detect_audio_request(user_message: str) -> bool:
    """
    Detect if user is requesting audio response
    
    Args:
        user_message: User's input message
        
    Returns:
        True if audio is requested, False otherwise
    """
    user_lower = user_message.lower()
    
    # Check for explicit audio/voice keywords
    audio_keywords = [
        'audio', 'voice', 'speak', 'sound', 'hear', 'listen', 
        'vocal', 'spoken', 'narrate'
    ]
    
    for keyword in audio_keywords:
        if keyword in user_lower:
            return True
    
    # Check for specific audio request phrases
    audio_phrases = [
        'with audio', 'in audio', 'as audio', 'audio please',
        'voice please', 'speak please', 'voice response', 
        'audio response', 'speak it', 'say it', 'read it',
        'read aloud', 'tell me with', 'speak the', 'say the'
    ]
    
    for phrase in audio_phrases:
        if phrase in user_lower:
            return True
    
    # Check for "tell me" only if it's followed by audio-related words
    if 'tell me' in user_lower:
        audio_context_words = ['with', 'in', 'voice', 'audio', 'speak', 'say']
        for word in audio_context_words:
            if f'tell me {word}' in user_lower:
                return True
    
    return False

def generate_audio_response(text: str, enable_tts: bool = True) -> str:
    """
    Generate audio response from text using TTS
    
    Args:
        text: Text to convert to speech
        enable_tts: Whether to enable TTS functionality
        
    Returns:
        Path to audio file if successful, empty string otherwise
    """
    if not enable_tts:
        return ""
    
    try:
        # Clean text for TTS (remove markdown formatting, etc.)
        clean_text = text.replace('**', '').replace('*', '').replace('\n', ' ')
        clean_text = ' '.join(clean_text.split())  # Remove extra whitespace
        
        # Generate audio
        audio_path = text_to_speech(clean_text, play_audio=True)
        
        if audio_path:
            print(f"🎵 Audio response generated: {audio_path}")
            return audio_path
        else:
            print("⚠️  TTS generation failed, showing text only")
            return ""
            
    except Exception as e:
        print(f"⚠️  TTS error: {e}")
        return ""

def process_conversation(client, model, conversation_history, user_message, tools=tools, enable_tts: bool = True):
    """Process a single user message and return the updated history and response"""
    encoding = tiktoken.get_encoding("cl100k_base")  # Hoặc chọn tokenizer phù hợp
    token_count = len(encoding.encode(user_message))

    if token_count > MAX_TOKENS:
        error_message = f"Error: Your request is too long ({token_count} tokens). Please keep it under {MAX_TOKENS} tokens."
        conversation_history.append({"role": "assistant", "content": error_message})
        return conversation_history, error_message

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
        # print(final_content)
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
            
            # print(f"AI: {final_content}")
            
        except openai.APIError as e:
            # print(f"API error in final response: {e}")
            final_content = f"Error: {str(e)}"
    else:
        # If no tool calls were processed, the first response might already have content
        if response.choices[0].message.content and not final_content:
            final_content = response.choices[0].message.content
            # print(f"AI: {final_content}")

    # Generate audio response only if TTS is enabled, we have content, and user requested audio
    if final_content and enable_tts and detect_audio_request(user_message):
        generate_audio_response(final_content, enable_tts)

    return conversation_history, final_content