from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    filename: str  # which document to query against

class AskResponse(BaseModel):
    question: str
    answer: str
    filename: str

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if not request.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid filename")

    # placeholder — real RAG answer replaces this in Phase 3
    return AskResponse(
        question=request.question,
        answer="RAG pipeline not connected yet — coming in Phase 3",
        filename=request.filename
    )