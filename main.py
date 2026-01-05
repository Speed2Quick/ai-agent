import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():

    #read the api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("The API key was not found")

    #create the gemini instance
    client = genai.Client(api_key=api_key)

    #get the users prompt from the CL
    parser = argparse.ArgumentParser(description="Users prompt to the chatbot")
    parser.add_argument("user_prompt", type=str, help="Prompt to the chatbot")

    #toggle verbose
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    user_prompt = args.user_prompt

    #store the prompt and generate the response
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt,))

    if response is None:
        raise RuntimeError("The API generate content request failed")

    #get the used tokens
    user_prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    #output
    if args.verbose:
        print(f"Prompt tokens: {user_prompt_tokens}")
        print(f"Prompt: {user_prompt}")
        print(f"Response tokens: {response_tokens}")

    if not response.function_calls:
        print(f"Response: {response.text}")
        return

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")



if __name__ == "__main__":
    main()
