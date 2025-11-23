import re
import fitz            # PyMuPDF
import docx
import pandas as pd


def clean_text(text: str) -> str:
    """Normalize text by removing excessive whitespace and null characters."""
    text = re.sub(r"\s+", " ", text)
    return text.replace("\x00", "").strip()


# File Format Extractors
def extract_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = "".join(page.get_text() for page in doc)
    return clean_text(text)


def extract_docx(path: str) -> str:
    doc = docx.Document(path)
    text = "\n".join(p.text for p in doc.paragraphs)
    return clean_text(text)


def extract_csv(path: str) -> str:
    df = pd.read_csv(path)
    return clean_text(df.to_string())


# Smart Text Chunking
def chunk_text(text: str, size: int = 500, overlap: int = 100):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap

    return chunks


# Auto-Detect Extractor
def extract_text(path: str) -> list[str]:
    """Auto-detect file type, extract text, and chunk it."""
    path_l = path.lower()

    if path_l.endswith(".pdf"):
        text = extract_pdf(path)
    elif path_l.endswith(".docx"):
        text = extract_docx(path)
    elif path_l.endswith(".csv"):
        text = extract_csv(path)
    else:
        raise ValueError("Unsupported file format")

    return chunk_text(text)
