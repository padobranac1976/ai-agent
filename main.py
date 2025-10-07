import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info
def main():    
    load_dotenv()
    model_name = "gemini-2.0-flash-001"
    arguments = sys.argv
    
    if len(arguments) < 2:
        print("Error: prompt for the LLM is missing. Please enter text to pass onto the LLM as a string.")
        sys.exit(1)
        
    user_prompt = sys.argv[1]
    verbose = False
    if len(arguments) == 3 and arguments[2] == "--verbose":
        verbose = True
    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    client = genai.Client(api_key=api_key)    
    
    response = client.models.generate_content(model=model_name, contents=messages)
    print(response.text)
    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
