import numpy as np
import json
import openai


openai.api_key = "**********************************"

# Load pre-generated embeddings
embeddings_file = "data\embeddings.json"

def load_embeddings(file_path):
    with open(file_path, mode="r") as file:
        return json.load(file)

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search_query(query, embeddings, embedding_model="text-embedding-ada-002"):
    # Generate embedding for the query
    print("Generating embedding for the query...")
    response = openai.Embedding.create(input=query, model=embedding_model)
    query_embedding = response["data"][0]["embedding"]

    # Find the most relevant prompt
    max_similarity = -1
    most_similar_prompt = None

    for entry in embeddings:
        similarity = cosine_similarity(query_embedding, entry["embedding"])
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_prompt = entry["prompt"]

    return most_similar_prompt

# Example Usage
def query_example():
    print("Loading embeddings...")
    embeddings = load_embeddings(embeddings_file)

    print("Enter a query:")
    query = input("> ")

    result = search_query(query, embeddings)
    print("\nMost relevant prompt:")
    print(result)

if __name__ == "__main__":
    query_example()
