import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
  abs_working_directory = os.path.abspath(working_directory)
  abs_target_filepath = os.path.abspath(os.path.join(abs_working_directory, file_path))
  
  if not abs_target_filepath.startswith(abs_working_directory):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

  if not os.path.isfile(abs_target_filepath):
    return f'Error: File not found or is not a regular file: "{file_path}"'
  
  try:
    with open(abs_target_filepath, "r") as f:
      file_content = f.read(MAX_CHARS + 1)
      
      if len(file_content) > MAX_CHARS:
        file_content = file_content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
    return file_content
  except Exception as err:
    return f"Error: Unexpected error reading file {file_path}: {err}"