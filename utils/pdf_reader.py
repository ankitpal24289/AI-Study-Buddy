"""
Utilities for extracting text from uploaded files.
Supports: PDF, DOCX, TXT
"""

import io
from typing import Union


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all text from a PDF file (as bytes).
    Uses pdfplumber for best accuracy on complex layouts.
    Falls back to PyPDF2 if pdfplumber fails.
    """
    text = ""

    # Try pdfplumber first (better quality)
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages_text = []
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    pages_text.append(f"--- Page {i + 1} ---\n{page_text}")
            text = "\n\n".join(pages_text)
        if text.strip():
            return text
    except Exception:
        pass

    # Fallback to PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                pages_text.append(f"--- Page {i + 1} ---\n{page_text}")
        text = "\n\n".join(pages_text)
    except Exception as e:
        raise RuntimeError(f"Could not extract text from PDF: {e}")

    return text


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        raise RuntimeError(f"Could not extract text from DOCX: {e}")


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode a plain text file."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1")


def extract_text(uploaded_file) -> str:
    """
    Auto-detect file type from a Streamlit UploadedFile object
    and return extracted text.
    """
    name = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif name.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {uploaded_file.name}. Please upload PDF, DOCX, or TXT.")


def chunk_text(text: str, max_tokens: int = 3000, overlap: int = 200) -> list[str]:
    """
    Split text into chunks of roughly max_tokens words with overlap.
    This prevents hitting the LLM context window limit for long documents.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + max_tokens
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap  # overlap for context continuity

    return chunks
