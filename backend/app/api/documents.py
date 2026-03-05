"""Documents API endpoints"""

from fastapi import APIRouter, HTTPException
from app.services.qdrant_client import get_client, QDRANT_COLLECTION

router = APIRouter()


@router.get("/documents")
async def list_documents(tenant_id: str = "demo"):
    """List all documents for a tenant"""
    client = get_client()
    
    # Scroll all points for tenant
    results = client.scroll(
        collection_name=QDRANT_COLLECTION,
        scroll_filter={
            "must": [
                {"key": "tenant_id", "match": {"value": tenant_id}}
            ]
        },
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )
    
    # Group by doc_id
    docs = {}
    for point in results[0]:
        doc_id = point.payload.get("doc_id")
        if doc_id not in docs:
            docs[doc_id] = {
                "doc_id": doc_id,
                "filename": point.payload.get("filename"),
                "chunks": 0,
                "pages": set(),
            }
        docs[doc_id]["chunks"] += 1
        docs[doc_id]["pages"].add(point.payload.get("page", 0))
    
    # Convert to list
    result = []
    for doc in docs.values():
        doc["pages"] = len(doc["pages"])
        result.append(doc)
    
    return {"documents": result}


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, tenant_id: str = "demo"):
    """Delete a document and all its chunks"""
    client = get_client()
    
    # Delete by filter
    client.delete(
        collection_name=QDRANT_COLLECTION,
        points_selector={
            "filter": {
                "must": [
                    {"key": "doc_id", "match": {"value": doc_id}},
                    {"key": "tenant_id", "match": {"value": tenant_id}},
                ]
            }
        },
    )
    
    return {"success": True, "message": f"Document {doc_id} deleted"}
