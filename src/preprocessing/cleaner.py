"""Text normalization, tokenization, and cleaning for DAA Plagiarism Finder.

Adheres strictly to the specification:
- Convert text to lowercase
- Ignore punctuation
- Preserve raw character offsets for authentic visual highlighting
- Handle empty, invalid, or short documents gracefully
"""

import re
import string
from typing import List, Tuple, Optional
from src.algorithms.common import Token


# Pattern to identify individual words while tracking positions
WORD_REGEX = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")


def normalize_text(text: Optional[str]) -> str:
    """Normalize input text by converting to lowercase and stripping punctuation.
    
    Args:
        text: Raw text string (may be None or empty)
        
    Returns:
        Cleaned lowercase string with punctuation replaced by single spaces.
    """
    if not text:
        return ""
    # Convert to lowercase
    lower_text = text.lower()
    # Replace punctuation characters with whitespace
    translation_table = str.maketrans(string.punctuation, " " * len(string.punctuation))
    cleaned = lower_text.translate(translation_table)
    # Collapse multiple whitespaces into a single space
    return " ".join(cleaned.split())


def tokenize_text(text: Optional[str]) -> List[Token]:
    """Tokenize raw text into a list of Token objects with character coordinate mapping.
    
    Each Token retains:
    - text: normalized lowercase word
    - original_text: exact substring from input text
    - char_start, char_end: character slice in the original input string
    - index: 0-based sequential word index
    
    Args:
        text: Raw input text
        
    Returns:
        List of Token instances
    """
    if not text or not isinstance(text, str):
        return []
        
    tokens: List[Token] = []
    idx = 0
    for match in WORD_REGEX.finditer(text):
        raw_word = match.group(0)
        start, end = match.span()
        norm_word = raw_word.lower()
        if norm_word:
            tokens.append(Token(
                text=norm_word,
                original_text=raw_word,
                char_start=start,
                char_end=end,
                index=idx
            ))
            idx += 1
            
    return tokens


def get_token_strings(tokens: List[Token]) -> List[str]:
    """Helper to extract normalized string list from token stream."""
    return [t.text for t in tokens]


def validate_document_length(tokens: List[Token], k: int) -> Tuple[bool, str]:
    """Validate if token list satisfies minimum match length k.
    
    Args:
        tokens: List of Token objects
        k: Minimum match length (k-gram size)
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if k <= 0:
        return False, f"Minimum match length k must be positive (received k={k})."
    n = len(tokens)
    if n == 0:
        return False, "Document is empty or contains no readable words."
    if n < k:
        return False, f"Document has {n} words, which is fewer than minimum match length k={k}."
    return True, ""
