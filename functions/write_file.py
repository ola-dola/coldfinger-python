import os
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