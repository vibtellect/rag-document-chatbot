"""Ask API endpoints"""

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval import ask_question

router = APIRouter()


class AskRequest(BaseModel):
    question: str
    tenant_id: str = "demo"


class AskResponse(BaseModel):
    answer: str
    sources: list
    chunks_used: int


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    """
    Ask a question about uploaded documents
    
    - **question**: The question to answer
    - **tenant_id**: Tenant ID (default: "demo")
    """
    result = ask_question(
        question=req.question,
        tenant_id=req.tenant_id,
    )
    return result
