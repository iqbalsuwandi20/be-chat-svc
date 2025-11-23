import os
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    String, Integer, Boolean, TIMESTAMP, text
)
from sqlalchemy.orm import sessionmaker

# Load PostgreSQL config
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Build database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Metadata and table definition
metadata = MetaData()

documents_table = Table(
    "documents",
    metadata,
    Column("id", String, primary_key=True),
    Column("filename", String, nullable=False),
    Column("uploaded_at", TIMESTAMP, server_default=text("NOW()")),
    Column("chunk_count", Integer, nullable=False),
    Column("indexed", Boolean, default=False)
)

def init_db():
    metadata.create_all(engine)
