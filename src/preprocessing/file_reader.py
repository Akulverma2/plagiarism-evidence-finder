"""File extraction utilities for TXT, PDF, and DOCX documents."""

import os
import io
from typing import Union, Tuple


def extract_text_from_txt(content_bytes: bytes, encoding_candidates=("utf-8", "latin-1", "cp1252")) -> str:
    """Safely decode plain text bytes with fallback encodings."""
    for enc in encoding_candidates:
        try:
            return content_bytes.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    # Fallback with replacement of invalid characters
    return content_bytes.decode("utf-8", errors="replace")


def extract_text_from_pdf(content_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF (fitz) or pdfplumber."""
    # Attempt 1: PyMuPDF (fast and robust)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=content_bytes, filetype="pdf")
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        full_text = "\n".join(text_parts).strip()
        if full_text:
            return full_text
    except Exception:
        pass

    # Attempt 2: pdfplumber fallback
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
            full_text = "\n".join(pages).strip()
            if full_text:
                return full_text
    except Exception:
        pass

    # Attempt 3: pdfminer.six
    try:
        from pdfminer.high_level import extract_text
        extracted = extract_text(io.BytesIO(content_bytes))
        if extracted and extracted.strip():
            return extracted.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract readable text from PDF: {str(e)}")

    raise ValueError("PDF file appears to be empty, encrypted, or image-only scanned without OCR.")


def extract_text_from_docx(content_bytes: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        import docx
        doc = docx.Document(io.BytesIO(content_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
        return "\n".join(paragraphs)
    except Exception as e:
        raise ValueError(f"Could not read DOCX file: {str(e)}")


def read_uploaded_file(file_obj_or_path: Union[str, bytes, io.BytesIO], filename: str) -> Tuple[bool, str, str]:
    """Universal document reader supporting TXT, PDF, and DOCX.
    
    Args:
        file_obj_or_path: File path, bytes, or BytesIO stream
        filename: Name of the file with extension
        
    Returns:
        (success: bool, text_content: str, error_message: str)
    """
    if not filename:
        return False, "", "Filename is empty."

    ext = os.path.splitext(filename)[1].lower()

    # Read bytes
    try:
        if isinstance(file_obj_or_path, str):
            if not os.path.exists(file_obj_or_path):
                return False, "", f"File not found: {file_obj_or_path}"
            with open(file_obj_or_path, "rb") as f:
                content_bytes = f.read()
        elif isinstance(file_obj_or_path, bytes):
            content_bytes = file_obj_or_path
        elif hasattr(file_obj_or_path, "read"):
            content_bytes = file_obj_or_path.read()
            if hasattr(file_obj_or_path, "seek"):
                file_obj_or_path.seek(0)
        else:
            return False, "", f"Unsupported file input type: {type(file_obj_or_path)}"
    except Exception as e:
        return False, "", f"Error reading file bytes: {str(e)}"

    if not content_bytes:
        return False, "", "File is empty (0 bytes)."

    try:
        if ext in (".txt", ".text", ".md", ".csv", ".log"):
            text = extract_text_from_txt(content_bytes)
        elif ext == ".pdf":
            text = extract_text_from_pdf(content_bytes)
        elif ext in (".docx", ".doc"):
            if ext == ".doc":
                # Old binary .doc format is not directly docx
                return False, "", "Legacy .doc format is not supported; please convert to .docx or .pdf."
            text = extract_text_from_docx(content_bytes)
        else:
            return False, "", f"Unsupported file format '{ext}'. Supported: .txt, .pdf, .docx"

        if not text.strip():
            return False, "", "File parsed successfully but contains no extractable text."

        return True, text, ""
    except Exception as err:
        return False, "", str(err)
