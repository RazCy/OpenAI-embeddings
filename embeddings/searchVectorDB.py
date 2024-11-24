import numpy as np
import json
import openai
from pinecone import Pinecone


openai.api_key = "*****************************"
pc = Pinecone(api_key="******************************")

def search_in_pinecone(query, top_k=10, embedding_model="text-embedding-ada-002"):
    # Generate embedding for the query
    embedding_response = openai.Embedding.create(
        input=query,
        model=embedding_model
    )
    query_embedding = embedding_response["data"][0]["embedding"]
    index = pc.Index("application-management-qa")
    # Perform search in Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return results

# Example Query
query = "When was User Service deployed?"
results = search_in_pinecone(query)

# Print Results
for match in results["matches"]:
    print(f"Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")
 
