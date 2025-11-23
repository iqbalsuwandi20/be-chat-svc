from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os
import uuid
from pathlib import Path

# Services
from services.extractor import extract_text
from services.embedder import get_embedding
from services.retriever import search_similar
from services.llm_client import ask_llm

# Vector Store
from db.vector_store import add_embeddings

# PostgreSQL
from models.document import (
    save_document_metadata,
    mark_document_indexed,
    list_documents
)

# Redis Cache
from db.redis_cache import get_cache, set_cache

# Init DB
from db.postgres_conn import init_db, SessionLocal, documents_table


# Load env and init DB
load_dotenv()
init_db()

# Upload folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


app = FastAPI(
    title="Chat Knowledge Agent Backend",
    description="Backend for Document-based Q&A Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ChatRequest(BaseModel):
    doc_id: str
    question: str

class IndexRequest(BaseModel):
    doc_id: str
    chunks: List[str]

# Health Check Endpoint
@app.get("/health")
async def health_check():
    return {"status": "OK"}

# Chat Endpoint
@app.post("/chat")
async def chat(req: ChatRequest):
    cache_key = f"chat:{req.doc_id}:{req.question}"
    cached = get_cache(cache_key)

    if cached:
        return cached

    query_vec = await get_embedding(req.question)
    matches = search_similar(query_vec, req.doc_id, top_k=5)

    if not matches:
        result = {
            "question": req.question,
            "answer": "Tidak ditemukan data relevan di dokumen.",
            "context_used": [],
        }
        set_cache(cache_key, result)
        return result

    context = "\n\n".join(m["chunk"] for m in matches)
    answer = await ask_llm(req.question, context)

    result = {
        "question": req.question,
        "answer": answer,
        "context_used": matches,
    }

    set_cache(cache_key, result)
    return result

# Upload and extract text from document
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    doc_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{doc_id}.{ext}"

    with open(path, "wb") as f:
        f.write(await file.read())

    chunks = extract_text(path)

    save_document_metadata(
        doc_id=doc_id,
        filename=file.filename,
        chunk_count=len(chunks),
    )

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "chunks_count": len(chunks),
        "chunks": chunks,
    }

# Index document chunks
@app.post("/index")
async def index_document(payload: IndexRequest):
    embeddings = [await get_embedding(c) for c in payload.chunks]

    add_embeddings(payload.doc_id, embeddings, payload.chunks)
    mark_document_indexed(payload.doc_id)

    return {
        "doc_id": payload.doc_id,
        "chunks_indexed": len(payload.chunks),
        "status": "indexed successfully",
    }

# File Preview / Metadata
@app.get("/file/{doc_id}")
async def get_file_metadata(doc_id: str):
    db = SessionLocal()
    doc = db.query(documents_table).filter(documents_table.c.id == doc_id).first()

    if not doc:
        return JSONResponse({"error": "Document not found"}, status_code=404)

    return {
        "doc_id": doc_id,
        "filename": doc.filename,
        "url": f"http://127.0.0.1:8000/file/raw/{doc_id}"
    }

# Download Raw File
@app.get("/file/raw/{doc_id}")
async def download_file(doc_id: str):
    for file in os.listdir(UPLOAD_DIR):
        if file.startswith(doc_id):
            file_path = Path(f"{UPLOAD_DIR}/{file}")
            return FileResponse(file_path, media_type="application/pdf")

    return JSONResponse({"error": "File not found"}, status_code=404)

# List Documents
@app.get("/documents")
async def get_documents():
    return list_documents()


@app.get("/")
async def root():
    return {"message": "Chat Knowledge Agent Backend is running!"}
