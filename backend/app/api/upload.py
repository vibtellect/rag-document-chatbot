"""Upload API endpoints"""

import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ingestion import ingest_document

router = APIRouter()

ALLOWED_EXTENSIONS = (".pdf", ".md", ".markdown")
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    tenant_id: str = Form("demo"),
):
    """
    Upload and ingest a PDF or Markdown document.

    - **file**: PDF/MD file to upload
    - **tenant_id**: Tenant ID for multi-tenancy (default: "demo")
    """
    filename = file.filename or ""
    lower_name = filename.lower()

    if not lower_name.endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(400, "Only PDF and Markdown files are supported")

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(400, "Empty file")

    if len(contents) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, f"File too large (max {MAX_UPLOAD_SIZE_MB}MB)")

    try:
        result = ingest_document(
            file_bytes=contents,
            filename=filename,
            tenant_id=tenant_id,
        )
        return {
            "success": True,
            "message": "Document processed successfully",
            **result,
        }
    except ValueError as exc:
        raise HTTPException(400, f"Processing failed: {str(exc)}") from exc
    except Exception as exc:
        raise HTTPException(500, f"Processing failed: {str(exc)}") from exc
