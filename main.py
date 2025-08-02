import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    # verbose = False
    
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
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        
    print(res.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
    

if __name__ == "__main__":
    main()
