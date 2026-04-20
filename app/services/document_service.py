import os
import shutil
from fastapi import UploadFile
from PyPDF2 import PdfReader
import google.generativeai as genai
from app.core.config import settings

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Initialize Gemini for Vision/Multimodal extraction
genai.configure(api_key=settings.GOOGLE_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

def save_upload_file(upload_file: UploadFile, document_id: str) -> str:
    file_extension = os.path.splitext(upload_file.filename)[1]
    file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}{file_extension}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

async def extract_advanced_text(file_path: str) -> str:
    """
    Advanced extraction that handles tables and layout better.
    Uses Gemini 1.5 Flash to process the document if possible.
    """
    if not settings.GOOGLE_API_KEY:
        return extract_text_from_pdf(file_path)
    
    try:
        # For simplicity in this demo, we read the first few pages and use Gemini
        # In a full production app, we would use LlamaParse or convert PDF to images
        # Here we will use a hybrid approach: Text extraction + Gemini Cleanup
        raw_text = extract_text_from_pdf(file_path)
        
        prompt = f"""
        Below is raw text extracted from a financial document. 
        Please reformat it into clean Markdown, ensuring tables are correctly structured.
        If there are any obvious headers or sections, preserve them.
        
        RAW TEXT:
        {raw_text[:15000]} # Limiting context for Flash
        """
        
        # We use standard text generation for now to "clean" the OCR/Extracted text
        # If we had the PDF as a byte stream for Vision, we'd use that.
        response = await vision_model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"Advanced extraction failed, falling back to basic: {e}")
        return extract_text_from_pdf(file_path)

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
