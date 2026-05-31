from fastapi import APIRouter, UploadFile, File, HTTPException
import pdfplumber
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # check it's actually a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # save the file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # verify it's a readable PDF
    try:
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
    except Exception:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Could not read PDF file")

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "pages": page_count
    }