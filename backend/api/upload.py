from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from db.connection import get_db
from db.models import Document
import pdfplumber
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    contents = await file.read()

    MAX_SIZE = 10 * 1024 * 1024
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    def save_and_validate():
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        with pdfplumber.open(file_path) as pdf:
            return len(pdf.pages)

    try:
        page_count = await run_in_threadpool(save_and_validate)
    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail="Could not read PDF file")

    # save record to database
    document = Document(
        filename=file.filename,
        page_count=page_count
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "File uploaded successfully",
        "document_id": document.id,
        "filename": document.filename,
        "pages": document.page_count
    }