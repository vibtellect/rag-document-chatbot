"""Retrieval service: Question → Embedding → Search → Context"""

import os
from typing import List, Dict, Any
from app.services.qdrant_client import get_client, QDRANT_COLLECTION
from app.services.embeddings import get_embeddings
from app.services.llm import get_llm

RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))


def retrieve_context(
    question: str,
    tenant_id: str,
    top_k: int = RETRIEVAL_TOP_K,
) -> tuple[str, List[Dict]]:
    """
    Retrieve relevant context from Qdrant
    Returns: (context_text, sources)
    """
    # 1. Embed question
    embeddings = get_embeddings()
    query_vector = embeddings.embed(question)
    
    # 2. Search Qdrant with tenant filter
    client = get_client()
    results = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vector,
        query_filter={
            "must": [
                {"key": "tenant_id", "match": {"value": tenant_id}}
            ]
        },
        limit=top_k,
        with_payload=True,
    )
    
    if not results:
        return "", []
    
    # 3. Build context
    context_parts = []
    sources = []
    
    for r in results:
        context_parts.append(
            f"[Quelle: {r.payload['filename']}, Seite {r.payload['page']}]\n"
            f"{r.payload['text']}"
        )
        sources.append({
            "filename": r.payload["filename"],
            "page": r.payload["page"],
            "score": round(r.score, 3),
            "snippet": r.payload["text"][:200] + "...",
        })
    
    context = "\n\n---\n\n".join(context_parts)
    return context, sources


def ask_question(
    question: str,
    tenant_id: str,
    top_k: int = RETRIEVAL_TOP_K,
) -> Dict[str, Any]:
    """
    Full RAG pipeline: Question → Retrieve → Generate Answer
    """
    # 1. Retrieve context
    context, sources = retrieve_context(question, tenant_id, top_k)
    
    if not context:
        return {
            "answer": "Ich habe keine relevanten Dokumente zu dieser Frage gefunden. Bitte stellen Sie sicher, dass Dokumente hochgeladen wurden.",
            "sources": [],
            "chunks_used": 0,
        }
    
    # 2. Generate answer with Claude
    llm = get_llm()
    
    system_prompt = """Du bist ein hilfreicher Dokumenten-Assistent für Unternehmen. 
Beantworte die Frage AUSSCHLIEßLICH basierend auf dem bereitgestellten Kontext. 
Zitiere relevante Stellen mit [Quelle: Dateiname, Seite X]. 
Wenn die Antwort nicht im Kontext steht, sage das ehrlich."""
    
    user_prompt = f"""KONTEXT:
{context}

FRAGE: {question}

Beantworte die Frage basierend auf dem Kontext."""
    
    answer = llm.generate(
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.3,
    )
    
    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(sources),
    }
