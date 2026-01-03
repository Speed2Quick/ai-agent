import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        #check if file exists and is in the working directory
        is_valid_file_path = os.path.commonpath([abs_working_dir, target_file_path]) == abs_working_dir
        if is_valid_file_path == False:
            return f"Error: Cannot read \"{target_file_path}\" as it is outside the permitted working directory"
        if os.path.isfile(target_file_path) is False:
            return f"Error: File not found or is not a regular file: {target_file_path}"

        #read a max of 10000 characters from the file
        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += " [File \"{target_file_path}\" trucated at 10000 characters]"
        return content

    except Exception as e:
        return f"Error getting file contents: {e}"
