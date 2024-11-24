import openai
import pandas as pd
import json

# Set your OpenAI API Key
openai.api_key = "*******************************"

# Input and output file paths
xls_file = "data/application_management.xlsx"  # Replace with your Excel file name
output_file = "embeddings.json"

# Step 1: Read Excel File
def read_excel(file_path):
    print("Reading data from Excel file...")
    data = pd.read_excel(file_path)
    return data

# Step 2: Generate Prompts from DataFrame
def generate_prompts(dataframe):
    print("Generating prompts from data...")
    prompts = []
    for _, row in dataframe.iterrows():
        prompt = (
            f"Provide details about the application:\n"
            f"Application Name: {row['Application Name']}\n"
            f"Environment: {row['Environment']}\n"
            f"Tech Stack: {row['Tech Stack']}\n"
            f"Version: {row['Version']}\n"
            f"Deployed Date: {row['Deployed Date']}\n"
            f"Maintainer: {row['Maintainer']}\n"
            f"Status: {row['Status']}"
        )
        prompts.append(prompt)
    return prompts

# Step 3: Generate Embeddings
def generate_embeddings(prompts):
    embeddings = []
    for idx, prompt in enumerate(prompts):
        print(f"Generating embedding for prompt {idx + 1}/{len(prompts)}...")
        response = openai.Embedding.create(
            input=prompt,
            model="text-embedding-ada-002"
        )
        embeddings.append({
            "prompt": prompt,
            "embedding": response["data"][0]["embedding"]
        })
    return embeddings

# Step 4: Write Embeddings to JSON File
def write_to_json(embeddings, output_path):
    print(f"Writing embeddings to {output_path}...")
    with open(output_path, mode="w") as file:
        json.dump(embeddings, file, indent=4)
    print("Embeddings saved successfully.")

# Main Function
def main():
    # Step 1: Read XLS file
    dataframe = read_excel(xls_file)

    # Step 2: Generate Prompts
    prompts = generate_prompts(dataframe)

    # Step 3: Generate Embeddings
    embeddings = generate_embeddings(prompts)

    # Step 4: Save to JSON
    write_to_json(embeddings, output_file)

# Run the script
if __name__ == "__main__":
    main()
