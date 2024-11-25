import requests
import json

# Your OpenAI API key
API_KEY = "your-openai-api-key"

# OpenAI endpoint for chat completions
API_URL = "https://api.openai.com/v1/chat/completions"

def call_openai_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "gpt-4",  # or "gpt-3.5-turbo"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    }
    
    try:
        # Make a POST request to the OpenAI API
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Extract and return the assistant's reply
        reply = response.json()
        return reply["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except KeyError:
        return "Error: Unexpected response format."

# Main loop for user interaction
if __name__ == "__main__":
    print("Chat with OpenAI! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        reply = call_openai_api(user_input)
        print(f"GPT: {reply}")
