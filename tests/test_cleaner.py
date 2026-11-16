"""Unit tests for text normalization, tokenization, and cleaning."""

import pytest
from src.preprocessing.cleaner import (
    normalize_text,
    tokenize_text,
    get_token_strings,
    validate_document_length
)


def test_normalize_text():
    raw = "Hello, WORLD! This is a test... with punctuation; & symbols: 123."
    norm = normalize_text(raw)
    assert norm == "hello world this is a test with punctuation symbols 123"


def test_tokenize_text_coordinates():
    raw = "The quick fox."
    tokens = tokenize_text(raw)
    assert len(tokens) == 3

    assert tokens[0].text == "the"
    assert tokens[0].original_text == "The"
    assert tokens[0].char_start == 0
    assert tokens[0].char_end == 3
    assert tokens[0].index == 0

    assert tokens[1].text == "quick"
    assert tokens[1].original_text == "quick"
    assert tokens[1].char_start == 4
    assert tokens[1].char_end == 9
    assert tokens[1].index == 1

    assert tokens[2].text == "fox"
    assert tokens[2].original_text == "fox"
    assert tokens[2].char_start == 10
    assert tokens[2].char_end == 13
    assert tokens[2].index == 2


def test_contractions_and_hyphenation():
    raw = "Don't divide-and-conquer prematurely."
    tokens = tokenize_text(raw)
    words = get_token_strings(tokens)
    assert "don't" in words
    assert "divide" in words
    assert "and" in words
    assert "conquer" in words


def test_validate_document_length():
    tokens = tokenize_text("one two three")
    valid, msg = validate_document_length(tokens, k=3)
    assert valid
    assert msg == ""

    valid, msg = validate_document_length(tokens, k=5)
    assert not valid
    assert "fewer than minimum match length" in msg

    valid, msg = validate_document_length([], k=3)
    assert not valid
    assert "empty" in msg

    valid, msg = validate_document_length(tokens, k=0)
    assert not valid
    assert "positive" in msg
