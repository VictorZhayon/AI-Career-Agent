from PyPDF2 import PdfReader
import re

def parse_resume(uploaded_file):
    """Parse uploaded resume files (PDF or text)"""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text() or ""
                # Clean up common PDF parsing artifacts
                page_text = re.sub(r'\s+', ' ', page_text)
                text += page_text + "\n"
            return text.strip()
        
        elif uploaded_file.type == "text/plain":
            return uploaded_file.getvalue().decode("utf-8")
        
        else:
            raise ValueError("Unsupported file type")
            
    except Exception as e:
        raise RuntimeError(f"Resume parsing error: {str(e)}")