import os
import subprocess

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