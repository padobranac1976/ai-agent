import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info

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
    
    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    All paths you provide should be relative to the working directory. 
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    available_functions = types.Tool(function_declarations=[schema_get_files_info,])
    agent_config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    response = client.models.generate_content(model=model_name, 
                                              contents=messages,
                                              config=agent_config,
                                              )
    
    if response is None or response.usage_metadata is None:
        print("Response is malformed.")
        return
    
    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)    
    
if __name__ == "__main__":
    main()
