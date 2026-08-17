from pathlib import Path
import re

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF resume using PyMuPDF.
    """

    document = pymupdf.open(file_path)

    text = []

    for page in document:
        page_text = page.get_text("text")

        if page_text:
            text.append(page_text)

    document.close()

    result = "\n".join(text)

    # Remove the contact label "B" when it appears
    # immediately before an email address.
    result = re.sub(
        r'(?m)^B\s+(?=[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})',
        '',
        result
    )

    # Remove the contact label "H" when it appears
    # immediately before a phone number.
    result = re.sub(
        r'(?m)^H\s+(?=\+?\d[\d\s-]{7,})',
        '',
        result
    )

    return result


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX resume.
    """

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_resume_text(file_path: str) -> str:
    """
    Detect the resume file type and extract its text.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Please upload a PDF or DOCX resume."
        )