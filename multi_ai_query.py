import openai
import anthropic
import google.generativeai as genai
import threading
import os
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from .env file for security
load_dotenv()

# It's best practice to set your API keys as environment variables
# rather than hardcoding them directly in the script.
# Create a .env file in the same directory as this script and add:
# OPENAI_API_KEY="your_openai_api_key"
# ANTHROPIC_API_KEY="your_anthropic_api_key"
# GOOGLE_API_KEY="your_google_api_key"

openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- AI Model Functions ---

def get_openai_response(prompt, responses, model="gpt-4o"):
    """Gets a response from the OpenAI API."""
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        responses['OpenAI'] = response.choices[0].message.content
    except Exception as e:
        responses['OpenAI'] = f"Error: {e}"

def get_anthropic_response(prompt, responses, model="claude-3-opus-20240229"):
    """Gets a response from the Anthropic (Claude) API."""
    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        responses['Anthropic (Claude)'] = message.content[0].text
    except Exception as e:
        responses['Anthropic (Claude)'] = f"Error: {e}"

def get_google_response(prompt, responses, model="gemini-1.5-pro-latest"):
    """Gets a response from the Google (Gemini) API."""
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        responses['Google (Gemini)'] = response.text
    except Exception as e:
        responses['Google (Gemini)'] = f"Error: {e}"


def ask_ais(prompt):
    """Sends a prompt to multiple AIs and prints their responses."""
    responses = {}
    threads = []

    # --- Define the AI functions to call ---
    ai_functions = [
        get_openai_response,
        get_anthropic_response,
        get_google_response
    ]

    # --- Create and start a thread for each AI function ---
    for func in ai_functions:
        thread = threading.Thread(target=func, args=(prompt, responses))
        threads.append(thread)
        thread.start()

    # --- Wait for all threads to complete ---
    for thread in threads:
        thread.join()

    # --- Print the collected responses ---
    print("\n--- AI Responses ---")
    for ai, response in responses.items():
        print(f"\n--- {ai} ---\n")
        print(response)
    print("\n--------------------\n")


if __name__ == "__main__":
    print("Welcome to the Multi-AI Query Tool!")
    print("Type 'exit' to quit.")

    while True:
        user_question = input("Please enter your question: ")
        if user_question.lower() == 'exit':
            break
        ask_ais(user_question)
