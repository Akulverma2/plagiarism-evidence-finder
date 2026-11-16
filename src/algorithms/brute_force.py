"""Brute Force Baseline Plagiarism Detection Algorithm.

Course: Design and Analysis of Algorithms (DAA) - UPES Dehradun
Problem 17: Plagiarism Evidence Finder

This module implements the direct Brute Force algorithm:
1. Document Normalization & Tokenization (identical to D&C)
2. Direct nested comparison of suspect and source word sequences
3. Word comparison counting for each word equality check
4. Merging intervals using the identical merge logic
5. Exact similarity calculation producing identical evidence format
"""

import time
import tracemalloc
from typing import List, Tuple, Optional

from src.algorithms.common import Token, MatchInterval, EvidenceResult
from src.preprocessing.cleaner import normalize_text, tokenize_text, get_token_strings
from src.algorithms.divide_and_conquer import merge_intervals, calculate_similarity


def brute_force_find_matches(
    suspect_words: List[str],
    source_words: List[str],
    k: int,
    metrics: Optional[dict] = None
) -> List[Tuple[int, int, int, int]]:
    """Directly compares all k-word windows between suspect and source word lists.
    
    Time Complexity: O(N * M * k)
    Space Complexity: O(1) auxiliary space (no hash index)
    
    Args:
        suspect_words: Normalized suspect word list
        source_words: Normalized source word list
        k: Minimum match length
        metrics: Dictionary to collect comparison count
        
    Returns:
        List of matching window tuples: (suspect_start, suspect_end, source_start, source_end)
    """
    if metrics is None:
        metrics = {"comparisons": 0}

    n = len(suspect_words)
    m = len(source_words)
    if k <= 0 or n < k or m < k:
        return []

    raw_matches: List[Tuple[int, int, int, int]] = []

    # Outer loop: every valid suspect window start
    for i in range(n - k + 1):
        # Inner loop: every valid source window start
        for j in range(m - k + 1):
            is_match = True
            for offset in range(k):
                metrics["comparisons"] += 1
                if suspect_words[i + offset] != source_words[j + offset]:
                    is_match = False
                    break
            if is_match:
                raw_matches.append((i, i + k - 1, j, j + k - 1))

    return raw_matches


def run_brute_force(
    suspect_text: str,
    source_text: str,
    k: int = 3
) -> EvidenceResult:
    """Full execution pipeline for Brute Force plagiarism detection."""
    tracemalloc.start()
    start_time = time.perf_counter()

    suspect_tokens = tokenize_text(suspect_text)
    source_tokens = tokenize_text(source_text)

    suspect_words = get_token_strings(suspect_tokens)
    source_words = get_token_strings(source_tokens)

    total_suspect = len(suspect_words)
    total_source = len(source_words)

    metrics = {"comparisons": 0}

    raw_matches = brute_force_find_matches(suspect_words, source_words, k, metrics)
    merged_intervals = merge_intervals(raw_matches, suspect_tokens, source_tokens)
    copied_count, similarity_pct = calculate_similarity(merged_intervals, total_suspect)

    elapsed_time = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return EvidenceResult(
        algorithm_name="Brute Force",
        matches=merged_intervals,
        raw_window_matches=len(raw_matches),
        copied_word_count=copied_count,
        total_suspect_words=total_suspect,
        total_source_words=total_source,
        similarity_percentage=similarity_pct,
        execution_time_seconds=elapsed_time,
        comparison_count=metrics["comparisons"],
        memory_peak_kb=peak_memory / 1024.0
    )
