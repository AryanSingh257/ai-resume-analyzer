import pdfplumber
from docx import Document
import re

class TextExtractor:
    """Extract text from PDF and DOCX files"""
    
    def extract_from_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    def extract_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
    
    def extract_text(self, file_path):
        """Auto-detect file type and extract text"""
        if file_path.endswith('.pdf'):
            return self.extract_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self.extract_from_docx(file_path)
        else:
            print("Unsupported file format")
            return None
    
    def clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep essential punctuation
        text = re.sub(r'[^\w\s@.,()-]', '', text)
        return text.strip()
