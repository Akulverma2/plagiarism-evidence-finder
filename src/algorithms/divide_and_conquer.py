"""Divide and Conquer Plagiarism Detection Algorithm.

Course: Design and Analysis of Algorithms (DAA) - UPES Dehradun
Problem 17: Plagiarism Evidence Finder

This module implements the complete Divide and Conquer algorithm according to the
formal academic specifications:
1. Document Normalization & Tokenization
2. Source Document k-gram Hash Index Construction
3. Recursive Divide and Conquer on Suspect Document
   - Base case: range length < k words
   - Left half matches: [L, M)
   - Right half matches: [M, R)
   - Midpoint crossing matches: [M - k + 1, M - 1]
4. Exact Word Sequence Verification on Hash Collisions
5. Interval Merging for Overlapping / Contiguous Passages
6. Word Comparison Counting and Timing
7. Exact Similarity Percentage Calculation
"""

import time
import tracemalloc
from typing import List, Dict, Tuple, Set, Optional

from src.algorithms.common import Token, MatchInterval, EvidenceResult
from src.preprocessing.cleaner import normalize_text, tokenize_text, get_token_strings


def build_source_index(source_words: List[str], k: int) -> Dict[tuple, List[int]]:
    """Build a hash map index containing all k-word windows of the source document.
    
    Args:
        source_words: List of normalized words from the source document.
        k: Minimum match length (window size).
        
    Returns:
        Dict mapping k-word tuple -> list of starting indices in source_words.
    """
    index: Dict[tuple, List[int]] = {}
    m = len(source_words)
    if k <= 0 or m < k:
        return index

    for j in range(m - k + 1):
        window = tuple(source_words[j : j + k])
        if window not in index:
            index[window] = []
        index[window].append(j)

    return index


def verify_window_match(
    suspect_words: List[str],
    s_idx: int,
    source_words: List[str],
    src_idx: int,
    k: int,
    metrics: dict
) -> bool:
    """Perform exact word-by-word sequence verification and record comparison count."""
    for offset in range(k):
        metrics["comparisons"] += 1
        if suspect_words[s_idx + offset] != source_words[src_idx + offset]:
            return False
    return True


def find_crossing_matches(
    suspect_words: List[str],
    left: int,
    mid: int,
    right: int,
    k: int,
    source_index: Dict[tuple, List[int]],
    source_words: List[str],
    metrics: dict
) -> List[Tuple[int, int, int, int]]:
    """Find all matching k-word windows that cross the midpoint mid.
    
    A k-word window starting at index i spans [i, i + k - 1].
    It crosses the midpoint mid if and only if:
      - It starts before mid: i < mid  (i.e., i <= mid - 1)
      - It extends to or past mid: i + k - 1 >= mid (i.e., i >= mid - k + 1)
      
    Bound to the current subproblem [left, right):
      cross_start = max(left, mid - k + 1)
      cross_end   = min(right - k, mid - 1)
      
    Returns:
        List of raw matches as (suspect_start, suspect_end, source_start, source_end).
    """
    matches: List[Tuple[int, int, int, int]] = []
    cross_start = max(left, mid - k + 1)
    cross_end = min(right - k, mid - 1)

    if cross_start > cross_end:
        return matches

    for i in range(cross_start, cross_end + 1):
        window = tuple(suspect_words[i : i + k])
        candidate_sources = source_index.get(window)
        if candidate_sources:
            for j in candidate_sources:
                if verify_window_match(suspect_words, i, source_words, j, k, metrics):
                    matches.append((i, i + k - 1, j, j + k - 1))

    return matches


def divide_and_conquer(
    suspect_words: List[str],
    left: int,
    right: int,
    k: int,
    source_index: Dict[tuple, List[int]],
    source_words: List[str],
    metrics: dict
) -> List[Tuple[int, int, int, int]]:
    """Recursive Divide and Conquer algorithm to find all matching k-word windows.
    
    Recurrence:
        T(N) = 2 * T(N / 2) + O(k * lookups)
        
    Args:
        suspect_words: Full list of normalized suspect words.
        left: Starting index of current subproblem (inclusive).
        right: Ending index of current subproblem (exclusive).
        k: Window size.
        source_index: Precomputed k-gram hash map of source document.
        source_words: Full list of normalized source words.
        metrics: Dictionary holding execution statistics (comparisons, recursive calls).
        
    Returns:
        List of tuples: (suspect_start, suspect_end, source_start, source_end)
    """
    metrics["recursive_calls"] += 1
    length = right - left

    # Base Case: subproblem range is smaller than window size k
    if length < k:
        return []

    # Base Case: subproblem range is exactly equal to window size k (single window)
    if length == k:
        window = tuple(suspect_words[left : right])
        candidate_sources = source_index.get(window)
        matches = []
        if candidate_sources:
            for j in candidate_sources:
                if verify_window_match(suspect_words, left, source_words, j, k, metrics):
                    matches.append((left, right - 1, j, j + k - 1))
        return matches

    # Divide: compute midpoint
    mid = left + (length // 2)

    # Conquer: solve left and right halves recursively
    left_matches = divide_and_conquer(
        suspect_words, left, mid, k, source_index, source_words, metrics
    )
    right_matches = divide_and_conquer(
        suspect_words, mid, right, k, source_index, source_words, metrics
    )

    # Combine: check windows that cross the midpoint
    crossing_matches = find_crossing_matches(
        suspect_words, left, mid, right, k, source_index, source_words, metrics
    )

    return left_matches + crossing_matches + right_matches


def find_matches(
    suspect_words: List[str],
    source_words: List[str],
    k: int,
    metrics: Optional[dict] = None
) -> List[Tuple[int, int, int, int]]:
    """High-level entry point to find raw k-word matches using Divide and Conquer."""
    if metrics is None:
        metrics = {"comparisons": 0, "recursive_calls": 0}

    n = len(suspect_words)
    m = len(source_words)
    if k <= 0 or n < k or m < k:
        return []

    # Step 1: Build source index O(M)
    source_index = build_source_index(source_words, k)

    # Step 2: Run Divide and Conquer on suspect document O(N log N)
    raw_matches = divide_and_conquer(
        suspect_words, 0, n, k, source_index, source_words, metrics
    )

    return raw_matches


def merge_intervals(
    raw_matches: List[Tuple[int, int, int, int]],
    suspect_tokens: List[Token],
    source_tokens: List[Token]
) -> List[MatchInterval]:
    """Merge overlapping and contiguous k-word windows into maximal copied passages.
    
    If window at suspect i matches source j, and next window at suspect i+1 matches
    source j+1, they form an uninterrupted contiguous passage [s_start, s_end]
    matching [src_start, src_end].
    
    Args:
        raw_matches: List of (s_start, s_end, src_start, src_end)
        suspect_tokens: Token objects of suspect document
        source_tokens: Token objects of source document
        
    Returns:
        List of merged MatchInterval instances sorted by suspect_start.
    """
    if not raw_matches:
        return []

    # Deduplicate raw matches and sort by (suspect_start, source_start)
    unique_matches = sorted(list(set(raw_matches)), key=lambda x: (x[0], x[2]))

    merged: List[List[int]] = []  # [s_start, s_end, src_start, src_end]

    for s_start, s_end, src_start, src_end in unique_matches:
        if not merged:
            merged.append([s_start, s_end, src_start, src_end])
            continue

        prev = merged[-1]
        prev_s_start, prev_s_end, prev_src_start, prev_src_end = prev

        # Check if this window directly extends the previous passage:
        # 1. Suspect continues contiguously (s_start <= prev_s_end + 1)
        # 2. Source offset maintains the identical relative alignment:
        #    (s_start - prev_s_start) == (src_start - prev_src_start)
        offset_alignment = (s_start - prev_s_start) == (src_start - prev_src_start)

        if s_start <= prev_s_end + 1 and offset_alignment:
            # Extend previous passage
            prev[1] = max(prev[1], s_end)
            prev[3] = max(prev[3], src_end)
        else:
            merged.append([s_start, s_end, src_start, src_end])

    # Convert merged tuples into structured MatchInterval objects
    result_intervals: List[MatchInterval] = []
    for s_start, s_end, src_start, src_end in merged:
        matched_words = [t.text for t in suspect_tokens[s_start : s_end + 1]]
        matched_text = " ".join(matched_words)

        s_char_start = suspect_tokens[s_start].char_start
        s_char_end = suspect_tokens[s_end].char_end
        src_char_start = source_tokens[src_start].char_start
        src_char_end = source_tokens[src_end].char_end

        interval = MatchInterval(
            suspect_start=s_start,
            suspect_end=s_end,
            source_start=src_start,
            source_end=src_end,
            length=s_end - s_start + 1,
            matched_text=matched_text,
            suspect_char_start=s_char_start,
            suspect_char_end=s_char_end,
            source_char_start=src_char_start,
            source_char_end=src_char_end
        )
        result_intervals.append(interval)

    return result_intervals


def calculate_similarity(
    merged_intervals: List[MatchInterval],
    total_suspect_words: int
) -> Tuple[int, float]:
    """Calculate overall plagiarism similarity percentage.
    
    Similarity = (Number of unique copied suspect words / Total suspect words) * 100
    
    Ensures overlapping matching windows are merged into passages before calculating
    copied words. Does not count the same copied word more than once.
    
    Returns:
        Tuple of (copied_word_count: int, similarity_percentage: float rounded to 2 decimals)
    """
    if total_suspect_words <= 0 or not merged_intervals:
        return 0, 0.0

    copied_indices: Set[int] = set()
    for interval in merged_intervals:
        for idx in range(interval.suspect_start, interval.suspect_end + 1):
            copied_indices.add(idx)

    copied_word_count = len(copied_indices)
    percentage = round((copied_word_count / total_suspect_words) * 100, 2)
    return copied_word_count, percentage


def run_divide_and_conquer(
    suspect_text: str,
    source_text: str,
    k: int = 3
) -> EvidenceResult:
    """Full execution pipeline for Divide and Conquer plagiarism detection."""
    # Start tracking memory and time
    tracemalloc.start()
    start_time = time.perf_counter()

    suspect_tokens = tokenize_text(suspect_text)
    source_tokens = tokenize_text(source_text)

    suspect_words = get_token_strings(suspect_tokens)
    source_words = get_token_strings(source_tokens)

    total_suspect = len(suspect_words)
    total_source = len(source_words)

    metrics = {"comparisons": 0, "recursive_calls": 0}

    # Algorithm core execution
    raw_matches = find_matches(suspect_words, source_words, k, metrics)
    merged_intervals = merge_intervals(raw_matches, suspect_tokens, source_tokens)
    copied_count, similarity_pct = calculate_similarity(merged_intervals, total_suspect)

    elapsed_time = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return EvidenceResult(
        algorithm_name="Divide and Conquer",
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
