from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool
import pdfplumber
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    contents = await file.read()

    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

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

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "pages": page_count
    }