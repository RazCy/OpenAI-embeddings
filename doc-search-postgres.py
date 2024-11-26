import openai
import psycopg2
import tiktoken
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity

# Set your OpenAI API key
openai.api_key = "**********************"

# PostgreSQL connection setup
conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="password",
            host="127.0.0.1",
            port=5432,
)
cursor = conn.cursor()

# Create table to store text chunks and embeddings
def setup_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_embeddings (
        id SERIAL PRIMARY KEY,
        chunk TEXT,
        -- embedding VECTOR(1536)  -- Use the correct dimension for text-embedding-ada-002
        embedding FLOAT8[]  -- Use an array to store the embedding
    );
    """)
    conn.commit()

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

# Insert chunks and embeddings into the database
def store_embeddings_in_postgres(chunks):
    for chunk in chunks:
        # Generate embedding for the chunk
        response = openai.Embedding.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        embedding = response['data'][0]['embedding']

        # Insert into PostgreSQL
        cursor.execute(
            "INSERT INTO document_embeddings (chunk, embedding) VALUES (%s, %s);",
            (chunk, embedding)
        )
    conn.commit()

# Query the database for the most relevant chunk
def query_postgres(query):
    # Generate embedding for the query
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = response['data'][0]['embedding']

    # Query PostgreSQL for the most similar embedding
    cursor.execute(
        """
        SELECT chunk,embedding <-> %s AS distance
        FROM document_embeddings
        ORDER BY distance ASC
        LIMIT 1;
        """,
        (query_embedding,)
    )
    cursor.execute("SELECT chunk, embedding FROM document_embeddings;")
    #result = cursor.fetchone()
    result = cursor.fetchall()
    # Compute similarity
    max_similarity = -1
    most_similar_chunk = None
    for row in result:
        chunk, stored_embedding = row
        similarity = cosine_similarity([query_embedding], [stored_embedding])[0][0]
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_chunk = chunk
    #return result[0] if result else None
    return most_similar_chunk if most_similar_chunk else None

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
    # Set up the database
    setup_database()

    # Load your document
    with open("data/document.txt", "r") as file:
        document = file.read()

     # Split the document into chunks
    chunks = split_into_chunks(document)

    # Store embeddings in PostgreSQL
    print("Storing embeddings into PostgreSQL...")
    store_embeddings_in_postgres(chunks)

    # Interactive loop for user queries
    print("Ask a question (type 'exit' to quit):")
    while True:
        query = input("Q: ")
        if query.lower() == 'exit':
            break

        # Find the most relevant chunk from PostgreSQL
        relevant_chunk = query_postgres(query)

        if not relevant_chunk:
            print("No relevant context found.")
            continue

        # Get the answer from the model
        answer = answer_question(query, relevant_chunk)
        print(f"A: {answer}")

if __name__ == "__main__":
    main()
