import os

def get_files_info(working_directory, directory="."):
  dir_path = os.path.join(working_directory, directory)
  
  if not os.path.exists(dir_path):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  if not os.path.isdir(dir_path):
    return f'Error: "{directory}" is not a directory'
  
  dir_contents = os.listdir(dir_path)
  for item in dir_contents:
    item_path = os.path.join(dir_path, item)
    print(f"{item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
  

if __name__ == '__main__':
  print(get_files_info("calculator", "."))
  
  