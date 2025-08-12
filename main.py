import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python, run_python_file

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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
    


def main():
    parser = argparse.ArgumentParser(description="Poor man's Claude Code")
    parser.add_argument("user_prompt", type=str, help="Prompt for the AI agent")
    parser.add_argument("--verbose", action="store_true", help="How detailed the logs should be")
    
    args = parser.parse_args()
    
    system_prompt =system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python,
        ]
    )

    # CLI arguments 
    user_prompt = args.user_prompt
    verbose = args.verbose
    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    
    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages, 
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
    except Exception as e:
        print(f"An error occured during the api call: {e}", file=sys.stderr)
        sys.exit(1)
        
    if res.function_calls:
        for function_call_part in res.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            
            if (not function_call_result.parts or not function_call_result.parts[0].function_response.response):
                raise Exception("Empty function call result")
            
            print(f"-> {function_call_result.parts[0].function_response.response}")
            
        
    print(res.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
    

if __name__ == "__main__":
    main()
