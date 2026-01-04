import os

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
