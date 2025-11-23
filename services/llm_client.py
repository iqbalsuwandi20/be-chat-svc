import os
import httpx

LLM_BASE = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = "gpt-oss-20b"

if not LLM_BASE:
    raise ValueError("Missing LLM_BASE_URL in environment variables.")
if not LLM_API_KEY:
    raise ValueError("Missing LLM_API_KEY in environment variables.")

LLM_URL = f"{LLM_BASE}/chat/completions"


async def ask_llm(question: str, context: str) -> str:
    """Send context + question to LLM and return generated answer."""
    
    prompt = (
        "You are a document assistant.\n"
        "Use ONLY the provided context to answer the question.\n"
        "If the answer is not in the context, reply:\n"
        "\"I cannot find the answer in the document.\"\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}"
    )

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(LLM_URL, json=payload, headers=headers)

    data = response.json()

    if response.status_code != 200:
        raise Exception(f"LLM HTTP {response.status_code}: {data}")

    if "choices" not in data or not data["choices"]:
        raise Exception(f"Invalid LLM response: {data}")

    choice = data["choices"][0]

    if "message" in choice and "content" in choice["message"]:
        return choice["message"]["content"]

    if "text" in choice:
        return choice["text"]

    raise Exception(f"Unsupported LLM response structure: {data}")
