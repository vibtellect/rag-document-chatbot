# RAG Document Chatbot (PoC)

German first README: [README.md](./README.md)

## 3-Minute Outcome

A runnable RAG stack for internal company documents:

`PDF/Markdown upload -> chunking + embeddings -> Qdrant -> grounded answers`

## Problem

Company knowledge is fragmented across files and hard to search.

## Solution

FastAPI + Qdrant + Bedrock pipeline that answers questions with source references.

## Architecture

- Frontend: React + Vite
- Backend: FastAPI
- Vector store: Qdrant
- Models: Bedrock Claude + Titan Embeddings

## Quickstart

```bash
make setup
make up
make smoke
```

Expected:

- API health at `http://localhost:8000/health`
- Frontend at `http://localhost:3000`

Stop:

```bash
make down
```

## End-to-End Test

Upload a demo document:

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@demo-docs/it-sicherheitsrichtlinie.md" \
  -F "tenant_id=demo"
```

Ask a question:

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the password policy?","tenant_id":"demo"}'
```

## API Endpoints

- `POST /api/upload` (PDF or Markdown)
- `POST /api/ask`
- `GET /api/documents`
- `DELETE /api/documents/{doc_id}`
- `GET /health`

## Limits

- No auth/RBAC
- No long-term observability layer
- Retrieval strategy intentionally minimal for PoC simplicity

## CTA

Need to turn this into a production knowledge assistant? [https://bojatschkin.de](https://bojatschkin.de)

Blogpost (UTM): [RAG chatbot with Bedrock](https://bojatschkin.de/blog/rag-chatbot-bedrock?utm_source=github&utm_medium=readme&utm_campaign=rag-chatbot-demo)
