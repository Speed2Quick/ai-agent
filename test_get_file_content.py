from functions.get_file_content import get_file_content

def test_get_file_content():
    content = get_file_content("calculator", "lorem.txt")
    print("Result for lorem.txt with truncation")
    print(content)
    print()

    content = get_file_content("calculator", "main.py")
    print("Result for code file main.py")
    print(content)
    print()

    content = get_file_content("calculator", "pkg/calculator.py")
    print("Result for code file calculator.py")
    print(content)
    print()

    content = get_file_content("calculator", "bin/cat")
    print("Result for file not in working directory")
    print(content)
    print()

    content = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for non-existant file")
    print(content)
    print()

test_get_file_content()
