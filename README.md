# 📌 Chat Knowledge Agent - Backend Documentation

Backend untuk aplikasi Document-based Q&A Agent menggunakan RAG (Retrieval Augmented Generation). User mengunggah dokumen (PDF/DOCX/CSV), sistem mengekstrak isi, mem‐chunk, membuat embedding, menyimpan ke ChromaDB, metadata ke PostgreSQL, dan query dioptimalkan dengan Redis cache.

## 🎥 Demo Video

🔗 [**Lihat Demo Video Aplikasi**](https://drive.google.com/drive/folders/1-3xaHuDsJ7JP2Q_BIutU7ELO8AyUpTQB?usp=sharing)

---

## ✨ Fitur Utama

| Fitur | Status |
|-------|--------|
| Upload file & extract text | ✔ |
| Smart chunking + embedding | ✔ |
| Simpan embeddings ke ChromaDB | ✔ |
| Query RAG berbasis doc_id | ✔ |
| Integrasi LLM untuk jawaban | ✔ |
| Redis caching untuk jawaban cepat | ✔ |
| PostgreSQL metadata dokumen | ✔ |
| Endpoint list documents | ✔ |
| PDF preview endpoint | ✔ |
| Swagger Documentation | ✔ `/docs` |

---

## 🛠 Teknologi yang Digunakan

| Komponen | Teknologi |
|----------|-----------|
| Framework Backend | FastAPI (Python) |
| Vector Database | ChromaDB |
| Embedding Service | Ebbge-m3 (custom embedding API) |
| LLM Model | gpt-oss-20b |
| Metadata Storage | PostgreSQL |
| Cache | Redis |
| Document Parsing | PyMuPDF, python-docx, pandas |
| HTTP Client | HTTPX |
| Container DB | Docker (PostgreSQL + Redis) |
| Deployment Test | Local environment |

---

## 🧱 Arsitektur

```text
User → FastAPI → Extractor → Embedder → ChromaDB
                               ↓
                           PostgreSQL (metadata)
                               ↓
                              Redis (cache)
                               ↓
                              LLM Model
```

---

## 📍 Endpoint API

### 1) Upload Document

```http
POST /upload
```

**Respons:**

```json
{
  "doc_id": "uuid",
  "filename": "example.pdf",
  "chunks_count": 25,
  "chunks": ["...", "..."]
}
```

### 2) Index Document

```http
POST /index
```

**Body:**

```json
{
  "doc_id": "uuid",
  "chunks": ["...", "..."]
}
```

### 3) Chat dengan RAG

```http
POST /chat
```

**Body:**

```json
{
  "doc_id": "uuid",
  "question": "Apa isi dokumen?"
}
```

### 4) List Documents

```http
GET /documents
```

**Contoh response:**

```json
[
  { "id": "...", "filename": "...", "chunk_count": 25, "indexed": true }
]
```

### 5) Preview File

```http
GET /file/{doc_id}
```

**Response** → PDF stream untuk viewer frontend.

### 6) Health Check

```http
GET /health
```

---

## 🗄 Database & Infrastruktur

### PostgreSQL (Docker)

```bash
docker run --name pg-rag -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=chat_knowledge_db -p 5432:5432 -d postgres
```

### Redis (Docker)

```bash
docker run --name redis-rag -p 6379:6379 -d redis
```

---

## 📦 Instalasi & Menjalankan Backend

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Jalankan FastAPI

```bash
uvicorn main:app --reload
```

### 3) Akses Swagger

```text
http://127.0.0.1:8000/docs
```

---

## 🔐 Environment (.env example)

```env
# ==== LLM CONFIG ====
LLM_API_KEY=xxxx
LLM_BASE_URL=http://10.12.120.43:8787/v1
EMBEDDING_BASE_URL=http://10.12.120.32:8142/v1/embeddings
VECTOR_DB=chroma

# ==== POSTGRES CONFIG ====
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=chat_knowledge_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

# ==== REDIS CONFIG ====
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

---

## 🧪 Testing Alur

| Langkah | Endpoint |
|---------|----------|
| Upload file | `POST /upload` |
| Index embeddings | `POST /index` |
| Cek list dokumen | `GET /documents` |
| Preview PDF | `GET /file/{doc_id}` |
| Chat & tanya dokumen | `POST /chat` |

---

## 🎯 Update Log Backend

| Perubahan | Status |
|-----------|--------|
| Endpoint `/documents` | DONE |
| Endpoint preview file `/file/{doc_id}` | DONE |
| Add list_documents import | DONE |
| Return metadata in JSON | DONE |
| Remove print debug & cleanup | DONE |
