"""Mandatory Reference Test for UPES DAA Plagiarism Evidence Finder.

Source:
the quick brown fox jumps over the lazy dog near the river bank

Suspect:
yesterday the quick brown fox jumps over a sleeping dog near the river bank today

k = 3

Expected:
- Passage 1: "the quick brown fox jumps over"
  Positions: 1–6
  Length: 6 words
- Passage 2: "dog near the river bank"
  Positions: 9–13
  Length: 5 words
Expected similarity: 73.33%
"""

import pytest
from src.algorithms.divide_and_conquer import run_divide_and_conquer
from src.algorithms.brute_force import run_brute_force


SOURCE_TEXT = "the quick brown fox jumps over the lazy dog near the river bank"
SUSPECT_TEXT = "yesterday the quick brown fox jumps over a sleeping dog near the river bank today"
K = 3


def test_reference_example_divide_and_conquer():
    """Verify Divide and Conquer produces exact UPES reference specification results."""
    result = run_divide_and_conquer(SUSPECT_TEXT, SOURCE_TEXT, k=K)

    # 1. Total word counts
    assert result.total_suspect_words == 15
    assert result.total_source_words == 13

    # 2. Number of passages
    assert len(result.matches) == 2

    # 3. Passage 1 verification
    p1 = result.matches[0]
    assert p1.matched_text == "the quick brown fox jumps over"
    assert p1.suspect_start == 1
    assert p1.suspect_end == 6
    assert p1.length == 6

    # 4. Passage 2 verification
    p2 = result.matches[1]
    assert p2.matched_text == "dog near the river bank"
    assert p2.suspect_start == 9
    assert p2.suspect_end == 13
    assert p2.length == 5

    # 5. Total copied words and similarity
    assert result.copied_word_count == 11
    assert result.similarity_percentage == 73.33


def test_reference_example_brute_force():
    """Verify Brute Force produces exact identical output to D&C on reference text."""
    result = run_brute_force(SUSPECT_TEXT, SOURCE_TEXT, k=K)

    assert result.total_suspect_words == 15
    assert result.total_source_words == 13
    assert len(result.matches) == 2

    p1 = result.matches[0]
    assert p1.matched_text == "the quick brown fox jumps over"
    assert p1.suspect_start == 1
    assert p1.suspect_end == 6
    assert p1.length == 6

    p2 = result.matches[1]
    assert p2.matched_text == "dog near the river bank"
    assert p2.suspect_start == 9
    assert p2.suspect_end == 13
    assert p2.length == 5

    assert result.copied_word_count == 11
    assert result.similarity_percentage == 73.33


def test_algorithm_parity_reference():
    """Verify exact equivalence between D&C and Brute Force results."""
    dc = run_divide_and_conquer(SUSPECT_TEXT, SOURCE_TEXT, k=K)
    bf = run_brute_force(SUSPECT_TEXT, SOURCE_TEXT, k=K)

    assert dc.similarity_percentage == bf.similarity_percentage
    assert dc.copied_word_count == bf.copied_word_count
    assert len(dc.matches) == len(bf.matches)

    for m_dc, m_bf in zip(dc.matches, bf.matches):
        assert m_dc.suspect_start == m_bf.suspect_start
        assert m_dc.suspect_end == m_bf.suspect_end
        assert m_dc.source_start == m_bf.source_start
        assert m_dc.source_end == m_bf.source_end
        assert m_dc.matched_text == m_bf.matched_text
        assert m_dc.length == m_bf.length
