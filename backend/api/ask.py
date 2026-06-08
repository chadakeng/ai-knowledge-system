from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.connections import get_db
from db.models import Document
from rag.retriever import retrieve_and_answer

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    document_id: int

class AskResponse(BaseModel):
    question: str
    answer: str
    document_id: int

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, db: Session = Depends(get_db)):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    document = db.query(Document).filter(
        Document.id == request.document_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    answer = retrieve_and_answer(request.question, request.document_id, db)

    return AskResponse(
        question=request.question,
        answer=answer,
        document_id=request.document_id
    )