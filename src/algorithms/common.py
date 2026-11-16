"""Common data models and definitions for Plagiarism Evidence Finder."""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Token:
    """Represents a tokenized word with mapping to original document coordinates."""
    text: str                  # Normalized word (lowercase, punctuation stripped)
    original_text: str         # Exact original word from raw input
    char_start: int            # Start character index in original raw text
    char_end: int              # End character index in original raw text
    index: int                 # 0-based word index in document token stream


@dataclass
class MatchInterval:
    """Represents a copied passage matching between suspect and source documents.
    
    Indices are 0-based INCLUSIVE to match UPES DAA specification:
    e.g. suspect_start=1, suspect_end=6 -> 6 words.
    """
    suspect_start: int
    suspect_end: int
    source_start: int
    source_end: int
    length: int = 0
    matched_text: str = ""
    suspect_char_start: int = 0
    suspect_char_end: int = 0
    source_char_start: int = 0
    source_char_end: int = 0

    def __post_init__(self):
        if self.length == 0 and self.suspect_end >= self.suspect_start:
            self.length = self.suspect_end - self.suspect_start + 1

    @property
    def suspect_slice(self) -> Tuple[int, int]:
        """Returns Python slice boundary [start, end) for suspect tokens."""
        return (self.suspect_start, self.suspect_end + 1)

    @property
    def source_slice(self) -> Tuple[int, int]:
        """Returns Python slice boundary [start, end) for source tokens."""
        return (self.source_start, self.source_end + 1)


@dataclass
class EvidenceResult:
    """Complete plagiarism analysis outcome produced by an algorithm."""
    algorithm_name: str
    matches: List[MatchInterval]
    raw_window_matches: int
    copied_word_count: int
    total_suspect_words: int
    total_source_words: int
    similarity_percentage: float
    execution_time_seconds: float
    comparison_count: int
    memory_peak_kb: float = 0.0

    def to_dict(self) -> dict:
        return {
            "algorithm": self.algorithm_name,
            "similarity_percentage": self.similarity_percentage,
            "copied_word_count": self.copied_word_count,
            "total_suspect_words": self.total_suspect_words,
            "total_source_words": self.total_source_words,
            "num_passages": len(self.matches),
            "raw_window_matches": self.raw_window_matches,
            "execution_time_sec": self.execution_time_seconds,
            "word_comparisons": self.comparison_count,
            "memory_peak_kb": self.memory_peak_kb,
        }
