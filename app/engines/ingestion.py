import pdfplumber
from pathlib import Path
import docx

# Extracts and cleans raw text from a PDF file using pdfplumber
def extract_text_from_pdf(file_path: str | Path) -> str:
    extracted_text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

    full_text = "\n".join(extracted_text)
    return full_text.replace("\x00", "").strip()

# Extracts and cleans raw text from a PDF file using python-docx
def extract_text_from_docx(file_path: str | Path) -> str:
    doc = docx.Document(file_path)
    extracted_text = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            extracted_text.append(text)

    full_text = "\n".join(extracted_text)
    return full_text.replace("\x00","").strip()

def extract_text(file_path: str | Path) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(path)
    elif ext == ".docx":
        text = extract_text_from_docx(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Only .pdf and .docx are supported.")

    if not text:
        raise ValueError(f"Failed to extract readable text from {path.name}. The file may be empty or ureadable.")

    return text        