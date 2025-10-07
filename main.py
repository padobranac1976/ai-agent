import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from config import MAX_ITERATIONS


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
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory. 
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    available_functions = types.Tool(function_declarations=[schema_get_files_info,
                                                            schema_get_file_content,
                                                            schema_write_file,
                                                            schema_run_python_file])
    agent_config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    
    for i in range(0, MAX_ITERATIONS):
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
        
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
        if response.function_calls:
            for function_call_part in response.function_calls:
                try:
                    result = call_function(function_call_part, verbose=verbose)
                    messages.append(result)
                    if verbose:
                        print(result.parts[0].function_response.response["result"])
                except Exception as e:
                    raise Exception("This does not work")
        else:
            # Final agent text message
            print(response.text)
            return
    
if __name__ == "__main__":
    main()
