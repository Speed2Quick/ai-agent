import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        #check if file exists and is in the working directory
        is_valid_file_path = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
        if is_valid_file_path == False:
            return f"Error: Cannot write to \"{abs_file_path}\" as it is outside the permitted working directory"
        if os.path.isdir(abs_file_path):
            return f"Error: Cannot write to \"{abs_file_path}\" as it is a directory"

        #write to the file
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)

        #feedback for the agent
        return f"Successfully wrote to \"{abs_file_path}\" ({len(content)} characters written)"
        
    except Exception as e:
        return f"Error failed to write to file {e}"

#create description of the functions use and how it should be called for the agent (working directory is passed by the user for safety)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content parameter to the specified file returning feedback if successful",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path declaring the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the specified file",
                ),
        },
        required=["file_path", "content"],
    ),
)
