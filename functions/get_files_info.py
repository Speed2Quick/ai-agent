import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        #check if taget_dir exists and is in the working directory
        is_valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if is_valid_target_dir == False:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        if os.path.isdir(target_dir) is False:
            return f"Error: {target_dir} is not a directory"

        #format and output output directory contents
        dir_contents = os.listdir(target_dir)
        dir_info = []
        for file in dir_contents:
            file_path = os.path.join(target_dir, file)

            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_info = f"- {file}: file_size={size} bytes, is_dir={is_dir}"
            dir_info.append(file_info)

        return "\n".join(dir_info)
    except Exception as e:
        return f"Error listing directory contents: {e}"
