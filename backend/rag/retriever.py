from .vector_store import search_schemes_vector


def retrieve_schemes(query: str, top_k: int = 3):

    results = search_schemes_vector(query, top_k=top_k)

    schemes = []

    if not results:
        return schemes

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for document, metadata in zip(documents, metadatas):
        schemes.append({
            "document": document,
            "metadata": metadata
        })

    return schemes