import os

def get_files_info(working_directory, directory="."):
  abs_working_directory = os.path.abspath(working_directory)
  abs_target_directory = os.path.abspath(os.path.join(abs_working_directory, directory))
    
  if not abs_target_directory.startswith(abs_working_directory):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  if not os.path.isdir(abs_target_directory):
    return f'Error: "{directory}" is not a directory'
  
  def stringify_metadata(name):
    content_path = os.path.join(abs_target_directory, name)
    return f"{name}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}"
  
  try:
    contents = os.listdir(abs_target_directory)
    return "\n".join(map(stringify_metadata, contents))
  except Exception as err:
    return f"Error listing files: {err}"
  