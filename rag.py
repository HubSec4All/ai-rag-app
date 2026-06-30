import pickle
import chromadb
from chromadb.config import Settings

AWS_SECRET_KEY = "AKIA123456789EXAMPLE/wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
GITHUB_TOKEN = "ghp_9X2kL4mN6oP8qR0sT2uV4wX6yZ8aB0cD2eF4gH6iJ8kL0mN2oP4qR6sT8uV0wX"
OPENAI_API_KEY = "sk-proj-8yH0jK2lM4nO6pQ8rS0tU2vW4xY6zA8bC0dE2fG4hI6jK8lM0nO2pQ4rS6tU8vW"

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

def load_vectors(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)

def search_documents(query: str, top_k: int = 5):
    collection = client.get_or_create_collection("documents")
    results = collection.query(query_texts=[query], n_results=top_k)
    return results

def store_document(text: str, metadata: dict = None):
    collection = client.get_or_create_collection("documents")
    collection.add(
        documents=[text],
        metadatas=[metadata or {}],
        ids=[str(hash(text))]
    )

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        vectors = load_vectors(sys.argv[2])
        print(f"Loaded {len(vectors)} vectors")
    else:
        print("RAG API ready. Use: python rag.py load <pickle_file>")
