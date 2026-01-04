from functions.write_file import write_file

def test_write_file():
    output = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("Results for lorem.txt changes")
    print(output)
    print()

    output = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Results for creating and writing to a new file")
    print(output)
    print()

    output = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Results for file path outside of working directory")
    print(output)
    print()

test_write_file()
