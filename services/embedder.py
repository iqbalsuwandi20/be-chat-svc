import os
import httpx
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_URL = os.getenv("EMBEDDING_BASE_URL")
EMBEDDING_MODEL = "ebbge-m3"


async def get_embedding(text: str):
    """Request embedding vector from the embedding service."""
    if not EMBEDDING_URL:
        raise ValueError("Missing EMBEDDING_BASE_URL in environment variables.")

    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(EMBEDDING_URL, json=payload)

    if response.status_code != 200:
        raise Exception(f"Embedding API Error: {response.text}")

    data = response.json()
    return data["data"][0]["embedding"]
