import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        #check if file exists and is in the working directory
        is_valid_file_path = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
        if is_valid_file_path == False:
            return f"Error: Cannot read \"{abs_file_path}\" as it is outside the permitted working directory"
        if os.path.isfile(abs_file_path) is False:
            return f"Error: File not found or is not a regular file: \"{abs_file_path}\""

        #read a max of 10000 characters from the file
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += " [File \"{abs_file_path}\" trucated at 10000 characters]"
        return content

    except Exception as e:
        return f"Error getting file contents: {e}"

#create description of the functions use and how it should be called for the agent (working directory is passed by the user for safety)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads from the specified file relative to the working directory, truncating the file at 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path declaring the file to be read from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
