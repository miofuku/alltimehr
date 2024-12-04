import os
from typing import Optional
from fastapi import UploadFile
import pytesseract
from pdf2image import convert_from_bytes
from docx import Document

async def extract_text_from_file(file: UploadFile) -> Optional[str]:
    """
    Extract text content from various file formats
    
    Args:
        file: Uploaded file object
    
    Returns:
        str: Extracted text content
        None: If extraction fails
    """
    try:
        content = await file.read()
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext == '.pdf':
            # Convert PDF to images and extract text
            images = convert_from_bytes(content)
            text = '\n'.join([pytesseract.image_to_string(img) for img in images])
            
        elif file_ext in ['.doc', '.docx']:
            # Extract text from Word document
            doc = Document(content)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            
        else:
            # For text files, decode directly
            text = content.decode('utf-8')
            
        return text.strip()
        
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        return None 