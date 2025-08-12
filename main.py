import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content(client, messages, verbose):
    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages, 
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
    except Exception as e:
        print(f"An error occured during the api call: {e}", file=sys.stderr)
        sys.exit(1)
        
    if verbose:
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        
    if not res.function_calls:
        return res.text 
    
    function_responses = []
    if res.function_calls:
        for function_call_part in res.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            
            if (not function_call_result.parts or not function_call_result.parts[0].function_response.response):
                raise Exception("Empty function call result")
            
            print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


def main():
    parser = argparse.ArgumentParser(description="Poor man's Claude Code")
    parser.add_argument("user_prompt", type=str, help="Prompt for the AI agent")
    parser.add_argument("--verbose", action="store_true", help="How detailed the logs should be")
    
    args = parser.parse_args()

    # CLI arguments 
    user_prompt = args.user_prompt
    verbose = args.verbose
    
    if verbose:
        print(f"User prompt: {user_prompt}")
    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    
    generate_content(client, messages, verbose)
    

if __name__ == "__main__":
    main()
