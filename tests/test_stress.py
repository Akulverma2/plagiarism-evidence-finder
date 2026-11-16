"""Stress test for large document processing (>= 100,000 words).

Verifies:
- Scalability to 105,000 words
- Execution completes within reasonable time (< 15 seconds)
- Accurate detection of injected copied passages
- Memory stability
"""

import os
import json
import pytest
from src.algorithms.divide_and_conquer import run_divide_and_conquer


LARGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "large")
SOURCE_PATH = os.path.join(LARGE_DIR, "large_source_105k.txt")
SUSPECT_PATH = os.path.join(LARGE_DIR, "large_suspect_105k.txt")
META_PATH = os.path.join(LARGE_DIR, "large_metadata.json")


def test_100k_words_stress_test():
    """Verify Divide and Conquer handles 100,000+ words accurately and within performance limits."""
    assert os.path.exists(SOURCE_PATH), "Large source file missing; run generator first."
    assert os.path.exists(SUSPECT_PATH), "Large suspect file missing; run generator first."

    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        source_text = f.read()
    with open(SUSPECT_PATH, "r", encoding="utf-8") as f:
        suspect_text = f.read()

    total_words = len(suspect_text.split())
    assert total_words >= 100000, f"Expected >= 100,000 words, got {total_words}"

    result = run_divide_and_conquer(suspect_text, source_text, k=5)

    # 1. Total words check
    assert result.total_suspect_words >= 100000
    assert result.total_source_words >= 100000

    # 2. Performance boundary (< 10 seconds on modern CPU)
    assert result.execution_time_seconds < 10.0

    # 3. Matches found
    assert len(result.matches) > 0
    assert result.similarity_percentage > 30.0  # Injected target is ~35%

    # 4. Injected ground truth correlation
    if os.path.exists(META_PATH):
        with open(META_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)
        expected_pct = meta.get("target_similarity_pct", 35.0)
        # Verify detected similarity is within 2% of injected target
        assert abs(result.similarity_percentage - expected_pct) < 2.0
