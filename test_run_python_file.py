from functions.run_python_file import run_python_file

def test_run_python_file():
    output = run_python_file("calculator", "main.py") # (should print the calculator's usage instructions)
    print("Result for running calculator/main.py with no values")
    print(output)
    print()

    output = run_python_file("calculator", "main.py", ["3 + 5"]) # (should run the calculator... which gives a kinda nasty rendered result)
    print("Result for running calculator/main.py with values")
    print(output)
    print()

    output = run_python_file("calculator", "tests.py") # (should run the calculator's tests successfully)
    print("Result for testing calculator")
    print(output)
    print()

    output = run_python_file("calculator", "../main.py") # (this should return an error)
    print("Result for running the file outside the working directory")
    print(output)
    print()

    output = run_python_file("calculator", "nonexistent.py") # (this should return an error)
    print("Result for running a non-existant file")
    print(output)
    print()

    output = run_python_file("calculator", "lorem.txt")
    print("Result for running a non-python file")
    print(output)
    print()

test_run_python_file()
