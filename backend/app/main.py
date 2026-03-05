"""
RAG Chatbot Backend API
FastAPI + Qdrant + AWS Bedrock
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import upload, ask, documents
from app.services.qdrant_client import init_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize on startup, cleanup on shutdown"""
    # Startup: Ensure Qdrant collection exists
    init_collection()
    yield
    # Shutdown cleanup if needed


app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation API with Qdrant and AWS Bedrock",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for frontend (configurable via ENV)
_default_origins = "http://localhost:3000,http://localhost:5173"
cors_origins = os.getenv("CORS_ORIGINS", _default_origins).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(ask.router, prefix="/api", tags=["ask"])
app.include_router(documents.router, prefix="/api", tags=["documents"])


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "rag-chatbot-api"}


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "upload": "/api/upload",
            "ask": "/api/ask",
            "documents": "/api/documents",
        },
    }
