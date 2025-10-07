from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from config import WORKING_DIR


def call_function(function_call_part:types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
        

    if function_call_part.name == "get_files_info":
        response = get_files_info(working_directory=WORKING_DIR, **function_call_part.args)
    elif function_call_part.name == "get_file_content":
        response = get_file_content(working_directory=WORKING_DIR, **function_call_part.args)
    elif function_call_part.name == "write_file":
        response = write_file(working_directory=WORKING_DIR, **function_call_part.args)
    elif function_call_part.name == "run_python_file":
        response = run_python_file(working_directory=WORKING_DIR, **function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
        
    final_result = types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_call_part.name,
                                response={"result": response},
                                )
                            ],
                        )
    return final_result
    
    
    