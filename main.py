import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai.live import _api_module

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
    args = parser.parse_args()
    user_prompt = args.user_prompt

    #generate the response
    response = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)

    if response is None:
        raise RuntimeError("The API generate content request failed")

    #get the used tokens
    user_prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {user_prompt_tokens}\n")
    print(f"Response: {response.text}")
    print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
