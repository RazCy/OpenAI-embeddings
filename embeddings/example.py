import openai

# Step 1: Set up your API key (replace 'your-api-key' with your actual key)
openai.api_key = '*********************************'

# Step 2: Define the model and the message for GPT
model = "gpt-4o-mini-2024-07-18"  # The model you want to use (e.g., gpt-4 or gpt-3.5-turbo)

# Step 3: Send a request to the OpenAI API
response = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},  # Optional system message
        {"role": "user", "content": "What is the capital of France?"},   # User's question
    ]
)

# Step 4: Print the response from the assistant
print(response['choices'][0]['message']['content'].strip())
