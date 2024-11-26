import openai
from pinecone import Pinecone, ServerlessSpec
import numpy as np
import tiktoken
from sklearn.metrics.pairwise import cosine_similarity


# Initialize OpenAI API
openai.api_key = "************************"  # Replace with your OpenAI API Key

pc = Pinecone(api_key="************************")
# Create or connect to a Pinecone index
index_name = "document-embeddings"

indexes = pc.list_indexes().get('indexes', [])
if len(indexes) >= 1 and indexes[0].get('name') == index_name:
     print(f"Index '{index_name}' already exists. Skipping creation.")
else:
    pc.create_index(
    name=index_name,
    dimension=1536, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)
 
index = pc.Index(index_name)


# Function to split a document into smaller chunks
def split_into_chunks(text, max_tokens=500):
    tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")   # Change encoding if needed
    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks

# Function to generate and store embeddings in Pinecone
def store_embeddings_in_pinecone(chunks):
    for i, chunk in enumerate(chunks):
        # Generate embedding for the chunk
        response = openai.Embedding.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        embedding = response['data'][0]['embedding']

        # Upsert into Pinecone
        index.upsert([(str(i), embedding, {"text": chunk})])

# Function to query Pinecone for the most relevant chunk
def query_pinecone(query):
    # Generate embedding for the query
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = response['data'][0]['embedding']

    # Query Pinecone
    results = index.query(vector=query_embedding, top_k=1, include_metadata=True)
    if results and results['matches']:
        return results['matches'][0]['metadata']['text']
    return None

# Function to answer the user's question
def answer_question(query, relevant_chunk):
    prompt = f"""
    You are a helpful assistant. Use the following context to answer the question:

    Context:
    {relevant_chunk}

    Question:
    {query}

    Answer:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# Main function to read a document, store embeddings, and respond to user queries
def main():
    # Load your document
    with open("data/document.txt", "r") as file:
        document = file.read()

    # Split the document into chunks
    chunks = split_into_chunks(document)

    # Store embeddings in Pinecone
    print("Storing embeddings into Pinecone...")
    store_embeddings_in_pinecone(chunks)

    # Interactive loop for user queries
    print("Ask a question (type 'exit' to quit):")
    while True:
        query = input("Q: ")
        if query.lower() == 'exit':
            break

        # Find the most relevant chunk from Pinecone
        relevant_chunk = query_pinecone(query)

        if not relevant_chunk:
            print("No relevant context found.")
            continue

        # Get the answer from the model
        answer = answer_question(query, relevant_chunk)
        print(f"A: {answer}")

if __name__ == "__main__":
    main()
