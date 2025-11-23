import chromadb

# Initialize persistent ChromaDB
chroma_client = chromadb.PersistentClient(path="vector_store")

collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)


def add_embeddings(doc_id: str, embeddings: list, chunks: list[str]):
    """Store embeddings and text chunks for a document."""
    try:
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=[{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))],
            documents=chunks
        )
    except Exception:
        pass  # silent fail, consistent with other modules


def search_similar(query_embedding: list, doc_id: str, top_k: int = 3):
    """Retrieve similar chunks for a specific document."""
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"doc_id": doc_id}
        )
    except Exception:
        return []

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    response = []
    for i in range(len(documents)):
        response.append({
            "chunk": documents[i],
            "score": distances[i],
            "metadata": metadatas[i],
        })

    return response
