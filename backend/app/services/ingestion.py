"""Document ingestion service: file -> chunks -> embeddings -> Qdrant"""

import io
import os
import uuid
import hashlib
from typing import List, Dict, Any
from pypdf import PdfReader

from app.services.qdrant_client import get_client, QDRANT_COLLECTION
from app.services.embeddings import get_embeddings

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))


def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, List[Dict[str, Any]]]:
    """Extract text from PDF with page tracking."""
    reader = PdfReader(io.BytesIO(file_bytes))
    full_text = ""
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        full_text += text + "\n"
        pages.append({"page": i + 1, "text": text})

    return full_text, pages


def extract_text_from_markdown(file_bytes: bytes) -> tuple[str, List[Dict[str, Any]]]:
    """Extract text from UTF-8 markdown/plain text input."""
    text = file_bytes.decode("utf-8", errors="replace")
    return text, [{"page": 1, "text": text}]


def extract_text(file_bytes: bytes, filename: str) -> tuple[str, List[Dict[str, Any]]]:
    """Route extraction depending on file extension."""
    lower = filename.lower()

    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if lower.endswith(".md") or lower.endswith(".markdown"):
        return extract_text_from_markdown(file_bytes)

    raise ValueError("Unsupported file format. Only PDF and Markdown are supported.")


def chunk_text(text: str, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Split text into chunks with overlap and best-effort page tracking."""
    words = text.split()
    chunks = []

    if not words:
        return chunks

    step = max(1, CHUNK_SIZE - CHUNK_OVERLAP)

    for i in range(0, len(words), step):
        chunk_words = words[i : i + CHUNK_SIZE]
        if len(chunk_words) < 10:
            continue

        chunk_body = " ".join(chunk_words)

        page_num = 1
        for page in pages:
            if chunk_body[:100] and chunk_body[:100] in page["text"]:
                page_num = page["page"]
                break

        chunks.append(
            {
                "text": chunk_body,
                "page": page_num,
            }
        )

    return chunks


def ingest_document(
    file_bytes: bytes,
    filename: str,
    tenant_id: str,
) -> Dict[str, Any]:
    """Full ingestion pipeline: file -> text -> chunks -> embeddings -> Qdrant."""
    full_text, pages = extract_text(file_bytes=file_bytes, filename=filename)

    chunks = chunk_text(full_text, pages)
    if not chunks:
        raise ValueError("No text could be extracted from the file")

    embeddings = get_embeddings()
    vectors = embeddings.embed_batch([c["text"] for c in chunks])

    doc_id = hashlib.md5(file_bytes).hexdigest()[:12]

    from qdrant_client.models import PointStruct

    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "doc_id": doc_id,
                    "tenant_id": tenant_id,
                    "filename": filename,
                    "chunk_index": i,
                    "page": chunk["page"],
                    "text": chunk["text"],
                },
            )
        )

    client = get_client()
    client.upsert(collection_name=QDRANT_COLLECTION, points=points)

    return {
        "doc_id": doc_id,
        "filename": filename,
        "tenant_id": tenant_id,
        "pages": len(pages),
        "chunks": len(chunks),
    }
