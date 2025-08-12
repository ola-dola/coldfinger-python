
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python, run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)


def call_function(function_call_part: types.FunctionCall, verbose=False):
  working_dir = "./calculator"
  function_name = function_call_part.name
  function_args = function_call_part.args or {}
  function_result = None
  
  if function_name is None:
      raise TypeError("Model returned a function with no name")

  if verbose:
      print(f"Calling function: {function_name}({function_args})")
  else:
      print(f"Calling function: {function_name}")
      
  available_functions_dict = {
      "get_files_info": get_files_info,
      "get_file_content": get_file_content,
      "write_file": write_file,
      "run_python_file": run_python_file,
  }
  
  if function_name not in available_functions_dict:
      return types.Content(
          role="tool",
          parts=[
              types.Part.from_function_response(
                  name=function_name,
                  response={"error": f"Unknown function: {function_name}"},
              )
          ],
      )
      
  
  function_result = available_functions_dict[function_name](working_dir, **function_args)
  
  
  return types.Content(
      role="tool",
      parts=[
          types.Part.from_function_response(
              name=function_name,
              response={"result": function_result},
          )
  ],
)
    
