"""Unit tests for interval merging and similarity calculations."""

import pytest
from src.algorithms.common import MatchInterval
from src.algorithms.divide_and_conquer import merge_intervals, calculate_similarity
from src.preprocessing.cleaner import tokenize_text


def test_merge_contiguous_intervals():
    suspect_text = "alpha beta gamma delta epsilon"
    source_text = "alpha beta gamma delta epsilon"
    s_tokens = tokenize_text(suspect_text)
    src_tokens = tokenize_text(source_text)

    # Raw matches for k=3:
    # [alpha beta gamma] -> [0..2] matching [0..2]
    # [beta gamma delta] -> [1..3] matching [1..3]
    # [gamma delta epsilon] -> [2..4] matching [2..4]
    raw = [
        (0, 2, 0, 2),
        (1, 3, 1, 3),
        (2, 4, 2, 4)
    ]

    merged = merge_intervals(raw, s_tokens, src_tokens)
    assert len(merged) == 1
    m = merged[0]
    assert m.suspect_start == 0
    assert m.suspect_end == 4
    assert m.source_start == 0
    assert m.source_end == 4
    assert m.length == 5
    assert m.matched_text == "alpha beta gamma delta epsilon"


def test_merge_disjoint_intervals():
    suspect_text = "one two three gap four five six"
    source_text = "one two three other four five six"
    s_tokens = tokenize_text(suspect_text)
    src_tokens = tokenize_text(source_text)

    # Disjoint matches
    raw = [
        (0, 2, 0, 2),  # [one two three]
        (4, 6, 4, 6)   # [four five six]
    ]

    merged = merge_intervals(raw, s_tokens, src_tokens)
    assert len(merged) == 2
    assert merged[0].suspect_start == 0
    assert merged[0].suspect_end == 2
    assert merged[1].suspect_start == 4
    assert merged[1].suspect_end == 6


def test_calculate_similarity_overlapping():
    intervals = [
        MatchInterval(suspect_start=0, suspect_end=5, source_start=0, source_end=5),
        MatchInterval(suspect_start=3, suspect_end=8, source_start=10, source_end=15),
    ]
    # Indices covered: [0..5] (6 words) and [3..8] (indices 3,4,5,6,7,8).
    # Union of indices: 0, 1, 2, 3, 4, 5, 6, 7, 8 -> 9 words!
    copied_count, sim_pct = calculate_similarity(intervals, total_suspect_words=10)
    assert copied_count == 9
    assert sim_pct == 90.0


def test_calculate_similarity_empty():
    copied_count, sim_pct = calculate_similarity([], total_suspect_words=10)
    assert copied_count == 0
    assert sim_pct == 0.0

    copied_count, sim_pct = calculate_similarity([MatchInterval(0, 2, 0, 2)], total_suspect_words=0)
    assert copied_count == 0
    assert sim_pct == 0.0
