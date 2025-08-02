import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python command on the python program written in the file_path. Returns output of program as string, or an error string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python program to be executed. Must be a .py file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional. Additional arguments to pass to the python command",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
        required=["file_path"]
    ),
)


def run_python_file(working_directory, file_path, args=[]):
  abs_working_directory = os.path.abspath(working_directory)
  abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
  timeout_seconds = 30
  
  if not abs_file_path.startswith(abs_working_directory):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

  if not os.path.exists(abs_file_path):
    return f'Error: File "{file_path}" not found.'
  
  if not abs_file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'
  
  try:
    result = subprocess.run(["python", abs_file_path, *args], cwd=abs_working_directory, timeout=timeout_seconds, capture_output=True, text=True)
    output = []

    if result.stdout:
      output.append(f"STDOUT: {result.stdout}")
    if result.stderr:
      output.append(f"STDERR: {result.stderr}")
    if not result.stdout and not result.stderr:
      output.append("No output produced")
    if result.returncode != 0:
      output.append(f"Process exited with code {result.returncode}")
    
    return "\n".join(output)
  
  except subprocess.TimeoutExpired:
    return f"Error: running python on {file_path} timed out after {timeout_seconds} seconds"
  except Exception as e:
    return f"Error: executing Python file: {e}"