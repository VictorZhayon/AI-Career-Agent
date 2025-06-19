from PyPDF2 import PdfReader

def parse_resume(uploaded_file):
    """Parse uploaded resume files (PDF or text)"""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = "\n".join([page.extract_text() for page in reader.pages])
            return text
        elif uploaded_file.type == "text/plain":
            return uploaded_file.getvalue().decode("utf-8")
        else:
            raise ValueError("Unsupported file type")
    except Exception as e:
        raise RuntimeError(f"Parsing failed: {str(e)}")