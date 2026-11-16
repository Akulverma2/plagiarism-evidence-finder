"""Unit tests for file reader module (TXT, PDF, DOCX)."""

import io
import pytest
from src.preprocessing.file_reader import (
    extract_text_from_txt,
    read_uploaded_file
)


def test_extract_text_from_txt_encodings():
    utf8_bytes = "Hello World — Testing DAA".encode("utf-8")
    assert extract_text_from_txt(utf8_bytes) == "Hello World — Testing DAA"

    latin1_bytes = "Café résumé".encode("latin-1")
    assert "Café" in extract_text_from_txt(latin1_bytes)


def test_read_uploaded_file_txt():
    content = b"The quick brown fox jumps over the lazy dog."
    bio = io.BytesIO(content)
    ok, text, err = read_uploaded_file(bio, "sample.txt")
    assert ok
    assert text.strip() == "The quick brown fox jumps over the lazy dog."
    assert err == ""


def test_read_uploaded_file_docx_generation():
    # Test creating and reading a real docx in memory using python-docx
    import docx
    doc = docx.Document()
    doc.add_paragraph("This is a test paragraph from Word document.")
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)

    ok, text, err = read_uploaded_file(bio, "test_doc.docx")
    assert ok
    assert "This is a test paragraph from Word document." in text


def test_read_uploaded_file_invalid_ext():
    content = b"\x00\x01\x02"
    bio = io.BytesIO(content)
    ok, text, err = read_uploaded_file(bio, "binary.bin")
    assert not ok
    assert "unsupported" in err.lower()
