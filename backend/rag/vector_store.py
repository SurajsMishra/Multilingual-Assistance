import chromadb
from .embedding import generate_embedding
client = chromadb.PersistentClient(path = "chroma_db")
collection = client.get_or_create_collection(name = "government_schemes")
def add_scheme(
    scheme_id:str,
    text:str,
    metadata: dict
):
    embedding= generate_embedding(text)
    collection.upsert(
        embeddings = [embedding],
        documents = [text],
        metadatas = [metadata],
        ids = [scheme_id]
    )
def search_schemes_vector(query: str,top_k: int = 3):
    query_embedding = generate_embedding(query)
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results=top_k,
        
    )
    return results 
    