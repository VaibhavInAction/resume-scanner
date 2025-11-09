"""
Resume parser that extracts text from PDF, DOCX, and TXT files.
Handles various file formats and encoding issues gracefully.
"""

import os
import re
from typing import Optional
import PyPDF2
import docx

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file with encoding detection."""
    try:
        # Try UTF-8 first
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except UnicodeDecodeError:
        # Fallback to latin-1 if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error extracting text from TXT: {e}")
            return ""
    except Exception as e:
        print(f"Error extracting text from TXT: {e}")
        return ""

def parse_resume(file_path: str) -> Optional[str]:
    """
    Main function to parse resume and extract text.
    Automatically detects file type and uses appropriate parser.
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        Extracted text as string, or None if parsing fails
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    print(f"Parsing resume: {os.path.basename(file_path)} ({file_extension})")
    
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        text = extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        text = extract_text_from_txt(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None
    
    if not text:
        print("Warning: No text extracted from resume")
        return None
    
    # Basic cleaning
    text = clean_text(text)
    
    print(f"Successfully extracted {len(text)} characters from resume")
    return text

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    Removes excessive whitespace and special characters.
    """
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\n.,;:!?@#()\-+=/]', '', text)
    
    return text.strip()

def extract_contact_info(text: str) -> dict:
    """
    Extract contact information from resume text.
    Returns email and phone number if found.
    """
    contact_info = {
        "email": None,
        "phone": None
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info["email"] = email_match.group(0)
    
    # Extract phone number (various formats)
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact_info["phone"] = phone_match.group(0)
    
    return contact_info
