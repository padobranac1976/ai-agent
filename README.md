AI-agent
========

This repository is a simple implementation of a CLI based ai-coding-agent. It uses google Gemini LLM under the hood and can run the following functions:
1. get_files_info
2. get_file_contents
3. write_file
4. run_python_file.

get_files_info
--------------
This function goes to a nominated directory and inspects all files (and subdirectories) returing their size and qualifier whether they are a directory or not

get_file_contents
-----------------
This function actually reads the files in the directory (which the agent needs to understand the code it is trying to fix)

write_file
----------
This function writes a new file (or overwrites the extising file with the same filename - CAREFUL!!!) with the given contents.

run_python_file
---------------
This function uses the python interpreter to execute the specified file.

Usage
=====
To use the coding agent you will need to put the code you are trying to fix in a separate directory inside the root directory. As an example there is already an implementation of a simple calculator.  

Be carefull when running the agent to try and restrict where it can write/execute functions so that it truly is restricted to the working directory. 

Also make sure that `config.py` file is adjusted to the correct working directory (default is `./caclulator`)

NOTE: The entire ai-agent is based on https://www.boot.dev/courses/build-ai-agent-python
