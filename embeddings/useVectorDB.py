import pandas as pd
import openai
from pinecone import Pinecone, ServerlessSpec

# Initialize OpenAI API
openai.api_key = "*********************************"  # Replace with your OpenAI API Key

pc = Pinecone(api_key="************************")
# Create or connect to a Pinecone index
index_name = "application-management-qa"

indexes = pc.list_indexes().get('indexes', [])
if len(indexes) == 1 and indexes[0].get('name') == index_name:
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
    

# Function to read Excel and store embeddings in Pinecone
def process_xls_and_store(file_path, embedding_model="text-embedding-ada-002"):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path,engine='openpyxl')
    index = pc.Index(index_name)
    prompts = []
    # Iterate through each row and create embeddings
    for _, row in df.iterrows():
        # Combine relevant columns to create a prompt
        row.index
        prompt = f"""
        Application ID:{row.index}
        Application Name: {row['Application Name']}
        Environment: {row['Environment']}
        Tech Stack: {row['Tech Stack']}
        Version: {row['Version']}
        Deployed Date: {row['Deployed Date']}
        Maintainer: {row['Maintainer']}
        Status: {row['Status']}
        """
        prompts.append(f"The {row['Application Name']} maintained by {row['Maintainer']}, is deployed in the {row['Environment']} environment with {row['Tech Stack']}.")
        prompts.append(f"Version {row['Version']} of {row['Application Name']}, deployed on {row['Deployed Date']}, is currently {row['Status']} status.")

        # Generate embedding
        '''
            response = openai.Embedding.create(
                input=prompt.strip(),
                model=embedding_model
            )
            embedding_vector = response["data"][0]["embedding"]
    
            # Insert into Pinecone
            index.upsert([
                {
                    "id": str(row['Application Name']).replace(" ", "_") + "_" + str({row.index}),  # Unique ID
                    "values": embedding_vector,
                    "metadata": {
                        "Application ID":row.index,
                        "Application Name": row['Application Name'],
                        "Environment": row['Environment'],
                        "Tech Stack": row['Tech Stack'],
                        "Version": row['Version'],
                        "Deployed Date": str(row['Deployed Date']),
                        "Maintainer": row['Maintainer'],
                        "Status": row['Status']
                    }
                }
            ])
        '''

        # Generate embeddings and upload to Pinecone
    for i, prompt_qa in enumerate(prompts):
     embedding = openai.Embedding.create(
        input=prompt_qa,
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]

    # Upload to Pinecone with metadata
     index.upsert([
        {
            "id": f"prompt_qa-{i+1}",
            "values": embedding,
            "metadata": {"prompt": prompt_qa}
        }
     ])

    print("Data successfully stored in Pinecone!")

# Provide the path to the Excel file
file_path = "data/application_management.xlsx"  # Replace with the actual file path
process_xls_and_store(file_path)
