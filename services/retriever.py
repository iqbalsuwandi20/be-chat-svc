import chromadb

# Persistent Chroma client
chroma_client = chromadb.PersistentClient(path="vector_store")

# Main document collection
collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)


def search_similar(query_embedding, doc_id: str, top_k: int = 3):
    """Return top-k most similar chunks from the specified document."""

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"doc_id": {"$eq": doc_id}}
    )

    docs = results.get("documents", [[]])
    metas = results.get("metadatas", [[]])
    scores = results.get("distances", [[]])

    if not docs or not docs[0]:
        return []

    return [
        {
            "chunk": chunk,
            "score": score,
            "metadata": meta
        }
        for chunk, meta, score in zip(docs[0], metas[0], scores[0])
    ]
