import os
import shutil
from fastapi import UploadFile
from PyPDF2 import PdfReader
from app.core.config import settings

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile, document_id: str) -> str:
    file_extension = os.path.splitext(upload_file.filename)[1]
    file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}{file_extension}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text
