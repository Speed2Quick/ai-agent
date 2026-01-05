import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        #check if file exists and is in the working directory abd is a python file
        is_valid_file_path = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
        if is_valid_file_path == False:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        if os.path.isfile(abs_file_path) is False:
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        if file_path[-3:] != ".py":
            return f"Error: \"{file_path}\" is not a Python file"

        #create command for subprocess
        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        #run subprocess with command
        result = subprocess.run(args=command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")         
        if not result.stdout and not result.stderr:
            output.append(f"No output produced")
        if result.stdout:
            output.append(f"STDOUT: \n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR: \n{result.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: Could not excecute python file {e}"

#create description of the functions use and how it should be called for the agent (working directory is passed by the user for safety)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file within the working directory with the required or optional args",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path declaring the python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array which holds the arguments to be passed to the function, default is None",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="An arguement to be passed to the function",
                    ),
                ),
        },
        required=["file_path"],
    ),
)
