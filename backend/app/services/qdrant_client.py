"""Qdrant client initialization and utilities"""

import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "documents")
VECTOR_SIZE = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))

_client = None


def get_client() -> QdrantClient:
    """Get or create Qdrant client (singleton)"""
    global _client
    if _client is None:
        _client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return _client


def init_collection():
    """Initialize Qdrant collection if not exists"""
    client = get_client()
    
    collections = [c.name for c in client.get_collections().collections]
    
    if QDRANT_COLLECTION not in collections:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
        print(f"Created collection: {QDRANT_COLLECTION}")
    else:
        print(f"Collection {QDRANT_COLLECTION} already exists")
