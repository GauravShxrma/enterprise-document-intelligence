import pytest 
import docx
from pathlib import Path
from app.engines.ingestion import extract_text

def test_extract_text_unsupported_file_type():
    with pytest.raises(ValueError) as exc_info:
        extract_text("sample.text")

    assert "Unsupported file format" in str(exc_info.value)

def test_extract_test_docx(tmp_path):
    docx_file = tmp_path/"test_resume.docx"

    doc = docx.Document()
    doc.add_paragraph("Python Backend Developer with 3 years of experience")
    doc.add_paragraph("skills: FastAPI, PostgreSQL, Docker")
    doc.save(docx_file)

    extracted = extract_text(docx_file)

    assert "Python Backend Developer" in extracted
    assert "FastAPI, PostgreSQL, Docker" in extracted

