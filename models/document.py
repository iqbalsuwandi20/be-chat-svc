from sqlalchemy import insert, update, select
from db.postgres_conn import engine, documents_table


def save_document_metadata(doc_id: str, filename: str, chunk_count: int):
    """Insert metadata dokumen ke PostgreSQL."""
    try:
        with engine.begin() as conn:
            conn.execute(
                insert(documents_table).values(
                    id=doc_id,
                    filename=filename,
                    chunk_count=chunk_count,
                    indexed=False
                )
            )
    except Exception:
        pass  # menjaga fail-silently sesuai pola modul lain


def mark_document_indexed(doc_id: str):
    """Tandai dokumen sudah ter-index."""
    try:
        with engine.begin() as conn:
            conn.execute(
                update(documents_table)
                .where(documents_table.c.id == doc_id)
                .values(indexed=True)
            )
    except Exception:
        pass


def get_document(doc_id: str):
    """Ambil metadata 1 dokumen."""
    try:
        with engine.begin() as conn:
            result = conn.execute(
                select(documents_table)
                .where(documents_table.c.id == doc_id)
            )
            return result.fetchone()
    except Exception:
        return None


def list_documents():
    try:
        with engine.begin() as conn:
            result = conn.execute(select(documents_table))
            rows = [dict(row._mapping) for row in result]
            return rows
    except Exception as e:
        return []

