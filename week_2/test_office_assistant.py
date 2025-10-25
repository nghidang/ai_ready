import os
import json
from pathlib import Path
import unittest
from unittest.mock import patch, Mock
from dotenv import load_dotenv
import openai
from office_assistant import SYSTEM_PROMPT, tools, process_conversation

# Load environment variables
load_dotenv()

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

class TestOfficeAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read configuration from environment variables
        cls.model = os.getenv('MODEL')
        cls.base_url = os.getenv('OPENAI_BASE_URL')
        cls.api_key = os.getenv('OPENAI_API_KEY')
        
        if not cls.model:
            raise ValueError("MODEL is not set in .env file")
        if not cls.base_url:
            raise ValueError("OPENAI_BASE_URL is not set in .env file")
        if not cls.api_key:
            raise ValueError("OPENAI_API_KEY is not set in .env file")
        
        cls.client = openai.OpenAI(
            base_url=cls.base_url,
            api_key=cls.api_key
        )
        
        # System prompt
        cls.system_prompt = SYSTEM_PROMPT
        
        # Directories
        cls.test_cases_dir = "test_cases"
        cls.responses_dir = "responses"
        
        # Create responses directory
        Path(cls.responses_dir).mkdir(exist_ok=True)

    def read_conversation_inputs(self, file_path):
        """Helper method to read conversation inputs from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.fail(f"File {file_path} not found")
        except Exception as e:
            self.fail(f"Error reading file: {str(e)}")
    
    def test_process_test_cases(self):
        """Test processing of all .txt files in test_cases directory."""
        if not os.path.exists(self.test_cases_dir):
            self.skipTest(f"Test cases directory {self.test_cases_dir} does not exist")
        
        for filename in os.listdir(self.test_cases_dir):
            if filename.endswith('.txt'):
                with self.subTest(filename=filename):
                    input_path = os.path.join(self.test_cases_dir, filename)
                    output_filename = os.path.splitext(filename)[0] + '.json'
                    output_path = os.path.join(self.responses_dir, output_filename)
                    
                    # Read conversation inputs
                    conversation_inputs = self.read_conversation_inputs(input_path)
                    self.assertGreater(len(conversation_inputs), 0, f"No valid inputs in {filename}")
                    
                    # Initialize conversation history
                    conversation_history = [
                        {
                            "role": "system",
                            "content": self.system_prompt
                        }
                    ]
                    
                    # Mock process_conversation to avoid actual API calls
                    with patch('office_assistant.process_conversation') as mock_process:
                        mock_process.return_value = (conversation_history, f"Mock response for {filename}")
                        
                        conversation_output = {}
                        for i, user_message in enumerate(conversation_inputs, 1):
                            # Simulate processing
                            updated_history, final_content = process_conversation(
                                self.client, self.model, conversation_history, user_message, tools
                            )
                            conversation_output[f"turn_{i}"] = {
                                "user": user_message,
                                "ai": final_content or "No response generated"
                            }
                            conversation_history = updated_history
                        
                        # Save output to JSON
                        try:
                            with open(output_path, "w", encoding="utf-8") as f:
                                json.dump(conversation_output, f, indent=2, ensure_ascii=False)
                            self.assertTrue(os.path.exists(output_path), f"Output file {output_path} was not created")
                        except Exception as e:
                            self.fail(f"Error saving conversation to JSON: {str(e)}")

if __name__ == '__main__':
    unittest.main()