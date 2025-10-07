import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path:str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        final_args = ["python3", abs_file_path]
        final_args += args
        output = subprocess.run(final_args,
                                cwd=abs_working_dir, 
                                timeout=30, 
                                capture_output=True)
        final_string = f"""
    STDOUT: {output.stdout}
    STDERR: {output.stderr}    
    """
        if output.stdout == "" and output.stderr == "":
            final_string = "No output produced."
        if output.returncode != 0:
            final_string += f"Error: Process exited with code {output.returncode}"
        return final_string
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified file with arguments using a python3 interpreter. Only files in the working directory can be exectuted.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory",),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",),},
        required=["file_path"]),)