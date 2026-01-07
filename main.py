import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from config import MAX_ITERS
from call_function import available_functions, call_function

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
    if args.verbose:
        print(f"Prompt: {user_prompt}")

    #store the prompt and generate the response
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(MAX_ITERS):
        try:
            response = generate_response(client, messages, args.verbose)
            if response:
                print()
                print(response)
                return
        except Exception as e:
            print(f"Error when generating response: {e}")

    print(f"Maximum interations {MAX_ITERS} for calling agent reached")
    sys.exit(1)

def generate_response(client, messages, verbose):
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt,))
    if response is None:
        raise RuntimeError("The API generate content request failed")

    #output
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    #track conversation history
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return f"Response: {response.text}"

    #handle and track function calling
    function_results = []
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise Exception("Empty function response for: {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_results.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_results))


if __name__ == "__main__":
    main()
