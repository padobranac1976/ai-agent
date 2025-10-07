from functions.run_python_file import run_python_file

def main():    
    working_dir = "calculator"    
    response = run_python_file(working_dir, "main.py")
    print(response)
    
    response = run_python_file("calculator", "main.py", ["3 + 5"])
    print(response)
    
    response = run_python_file("calculator", "tests.py")
    print(response)
    
    response = run_python_file("calculator", "../main.py")
    print(response)
    
    response = run_python_file("calculator", "nonexistent.py")
    print(response)
main()
    
    
    
