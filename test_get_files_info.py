from functions.get_files_info import get_files_info

def test_get_files_info():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print()

    result = get_files_info("calculator", "pkg")
    print("Result for pkg directory")
    print(result)
    print()

    result = get_files_info("calculator", "/bin")
    print("Result for directory outside of working path")
    print(result)
    print()

    result = get_files_info("calculator", "fake_dir")
    print("Result for non-existant directory")
    print(result)

test_get_files_info()
