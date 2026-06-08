import pdfplumber
import os

def extract_text_from_pdf(filename: str) -> str:
    file_path = os.path.join("uploads", filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    full_text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

    return "\n\n".join(full_text)