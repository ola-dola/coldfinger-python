import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content argument into the specified file in file_path. It overrites existing content if there is or creates new directories and files as needed otherwise",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file where content should be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
  abs_working_directory = os.path.abspath(working_directory)
  abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
  
  if not abs_file_path.startswith(abs_working_directory):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

  if not os.path.exists(abs_file_path):
    try:
      os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    except Exception as e:
      return f"Error creating new directory: {e}"
  
  if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
    return f"Error: {file_path} is not a file"
  
  try:
    with open(abs_file_path, 'w') as f:
      file_chars = f.write(content)
      return f'Successfully wrote to "{file_path}" ({file_chars} characters written)'
  except Exception as e:
    return f"Error writing to file: {e}"