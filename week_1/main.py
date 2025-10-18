import os
import json
from pathlib import Path
import openai

client = openai.OpenAI(
    base_url="https://aiportalapi.stu-platform.live/use",
    api_key="sk-amNWISclq5ZTRgAcgOBXzw"
)


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
            # Read the meeting transcript from file
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            # Create the prompt
            prompt = f"""
            Summarize the key points and action items from the following meeting transcript in a concise and organized manner. 
            Focus on the main discussion points, decisions made, and specific tasks assigned to each attendee, including deadlines where applicable. 
            The meeting transcript:\n\n{text}
            """

            response = client.chat.completions.create(
                model="GPT-5-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Get the response content
            result = response.choices[0].message.content
            print(result)
            
            # Write the result to a JSON file
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(result, file, indent=2, ensure_ascii=False)
                
            print(f"Processed {filename} -> {output_filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

print("\nAll files processed successfully!")
