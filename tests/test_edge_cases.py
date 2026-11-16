"""Comprehensive Edge Case Test Suite for Plagiarism Evidence Finder.

Tests all 15 mandatory edge cases required by the specification:
1. Empty suspect document
2. Empty source document
3. Documents shorter than k
4. Identical documents (100% similarity)
5. No matching sequences (0% similarity)
6. Repeated words
7. Multiple copied passages
8. Overlapping matches
9. Match crossing the midpoint
10. Match at the beginning
11. Match at the end
12. Invalid input
13. Unreadable / corrupt files
14. Scalability / large text sanity
15. Different k values
"""

import pytest
import os
import tempfile
from src.algorithms.divide_and_conquer import run_divide_and_conquer
from src.algorithms.brute_force import run_brute_force
from src.preprocessing.cleaner import normalize_text, tokenize_text, validate_document_length
from src.preprocessing.file_reader import read_uploaded_file


class TestEdgeCases:
    # 1. Empty suspect document
    def test_empty_suspect_document(self):
        source = "the quick brown fox jumps over the lazy dog"
        suspect = ""
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert dc.similarity_percentage == 0.0
        assert dc.copied_word_count == 0
        assert len(dc.matches) == 0
        assert dc.total_suspect_words == 0
        assert bf.similarity_percentage == 0.0
        assert bf.copied_word_count == 0

    # 2. Empty source document
    def test_empty_source_document(self):
        source = ""
        suspect = "the quick brown fox jumps over the lazy dog"
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert dc.similarity_percentage == 0.0
        assert dc.copied_word_count == 0
        assert len(dc.matches) == 0
        assert dc.total_source_words == 0
        assert bf.similarity_percentage == 0.0
        assert bf.copied_word_count == 0

    # 3. Documents shorter than k
    def test_documents_shorter_than_k(self):
        source = "hello world"  # 2 words
        suspect = "hello world"
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert dc.similarity_percentage == 0.0
        assert len(dc.matches) == 0
        assert bf.similarity_percentage == 0.0
        assert len(bf.matches) == 0

        # Also verify validation helper
        tokens = tokenize_text(source)
        valid, msg = validate_document_length(tokens, k=3)
        assert not valid
        assert "fewer than minimum match length" in msg

    # 4. Identical documents (100% similarity)
    def test_identical_documents(self):
        text = "algorithms and data structures are fundamental computer science concepts"
        dc = run_divide_and_conquer(text, text, k=3)
        bf = run_brute_force(text, text, k=3)

        assert dc.similarity_percentage == 100.0
        assert dc.copied_word_count == dc.total_suspect_words
        assert len(dc.matches) == 1
        assert dc.matches[0].suspect_start == 0
        assert dc.matches[0].suspect_end == dc.total_suspect_words - 1
        assert bf.similarity_percentage == 100.0
        assert bf.copied_word_count == dc.copied_word_count

    # 5. No matching sequences (0% similarity)
    def test_no_matching_sequences(self):
        source = "apple orange banana grape strawberry pineapple mango"
        suspect = "quantum physics relativity gravity mechanics thermodynamics"
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert dc.similarity_percentage == 0.0
        assert dc.copied_word_count == 0
        assert len(dc.matches) == 0
        assert bf.similarity_percentage == 0.0

    # 6. Repeated words
    def test_repeated_words(self):
        source = "buffalo buffalo buffalo buffalo buffalo buffalo"
        suspect = "buffalo buffalo buffalo buffalo"
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert dc.similarity_percentage == 100.0
        assert dc.copied_word_count == 4
        assert bf.similarity_percentage == 100.0
        assert bf.copied_word_count == 4

    # 7. Multiple copied passages
    def test_multiple_copied_passages(self):
        source = "alpha beta gamma delta epsilon zeta eta theta iota kappa"
        # Suspect copies [alpha beta gamma] and [zeta eta theta iota]
        suspect = "intro alpha beta gamma middle zeta eta theta iota conclusion"
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert len(dc.matches) == 2
        assert dc.matches[0].matched_text == "alpha beta gamma"
        assert dc.matches[0].suspect_start == 1
        assert dc.matches[0].suspect_end == 3

        assert dc.matches[1].matched_text == "zeta eta theta iota"
        assert dc.matches[1].suspect_start == 5
        assert dc.matches[1].suspect_end == 8

        assert dc.copied_word_count == 3 + 4  # 7 words out of 10 total
        assert dc.similarity_percentage == 70.0
        assert bf.similarity_percentage == 70.0

    # 8. Overlapping matches
    def test_overlapping_matches(self):
        # When a pattern matches multiple parts in source or contiguous overlap in suspect
        source = "one two three four five six"
        suspect = "one two three four five six"
        # k=2: windows are [one two], [two three], [three four], [four five], [five six]
        dc = run_divide_and_conquer(suspect, source, k=2)
        # Should merge into a single passage spanning all 6 words
        assert len(dc.matches) == 1
        assert dc.copied_word_count == 6
        assert dc.similarity_percentage == 100.0

    # 9. Match crossing the midpoint of suspect document
    def test_match_crossing_midpoint(self):
        # Total 10 words: midpoint is index 5
        # We place a match spanning indices 3, 4, 5, 6 (crossing midpoint 5)
        source = "unrelated words start here red blue green yellow and end here"
        # suspect has 10 words:
        # 0: wordA, 1: wordB, 2: wordC, 3: red, 4: blue, 5: green, 6: yellow, 7: wordD, 8: wordE, 9: wordF
        suspect = "worda wordb wordc red blue green yellow wordd worde wordf"
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert len(dc.matches) == 1
        assert dc.matches[0].matched_text == "red blue green yellow"
        assert dc.matches[0].suspect_start == 3
        assert dc.matches[0].suspect_end == 6
        assert dc.copied_word_count == 4
        assert dc.similarity_percentage == 40.0
        assert bf.similarity_percentage == dc.similarity_percentage

    # 10. Match at the beginning
    def test_match_at_beginning(self):
        source = "machine learning models require substantial training datasets and validation"
        suspect = "machine learning models require substantial unrelated extra random text"
        dc = run_divide_and_conquer(suspect, source, k=4)
        bf = run_brute_force(suspect, source, k=4)

        assert dc.matches[0].suspect_start == 0
        assert dc.matches[0].suspect_end == 4
        assert dc.matches[0].matched_text == "machine learning models require substantial"
        assert dc.copied_word_count == 5
        assert dc.similarity_percentage == round(5 / 9 * 100, 2)
        assert bf.similarity_percentage == dc.similarity_percentage

    # 11. Match at the end
    def test_match_at_end(self):
        source = "natural language processing with transformers and attention mechanisms"
        suspect = "some arbitrary preliminary discussion transformers and attention mechanisms"
        dc = run_divide_and_conquer(suspect, source, k=3)
        bf = run_brute_force(suspect, source, k=3)

        assert len(dc.matches) == 1
        assert dc.matches[0].suspect_end == dc.total_suspect_words - 1
        assert dc.matches[0].matched_text == "transformers and attention mechanisms"
        assert bf.similarity_percentage == dc.similarity_percentage

    # 12. Invalid input handling
    def test_invalid_input(self):
        # None, non-string, punctuation only, whitespace only
        assert normalize_text(None) == ""
        assert tokenize_text(None) == []
        assert tokenize_text("   \n\t  ") == []
        assert tokenize_text("!@#$%^&*()_+:;<>?") == []

        dc = run_divide_and_conquer("!@#$%", "hello world", k=3)
        assert dc.similarity_percentage == 0.0
        assert dc.copied_word_count == 0

    # 13. Unreadable / Corrupt file handling
    def test_unreadable_and_corrupt_files(self):
        # Non-existent file
        ok, text, err = read_uploaded_file("non_existent_file_xyz.txt", "non_existent_file_xyz.txt")
        assert not ok
        assert "not found" in err.lower()

        # Empty file
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            ok, text, err = read_uploaded_file(tmp_path, "empty.txt")
            assert not ok
            assert "empty" in err.lower()
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Unsupported extension
        ok, text, err = read_uploaded_file(b"dummy binary", "image.exe")
        assert not ok
        assert "unsupported" in err.lower()

    # 14. Scalability / Large document sanity
    def test_scalability_sanity(self):
        # Verify 1,000 distinct words runs cleanly and fast (< 1.0 second)
        words = [f"word{i}" for i in range(1000)]
        source_text = " ".join(words)
        # Suspect copies 400 words from middle
        suspect_words = ["intro"] + words[200:600] + ["outro"]
        suspect_text = " ".join(suspect_words)

        dc = run_divide_and_conquer(suspect_text, source_text, k=4)
        assert dc.execution_time_seconds < 1.0
        assert dc.copied_word_count == 400
        assert dc.total_suspect_words == 402
        assert dc.similarity_percentage == round(400 / 402 * 100, 2)

    # 15. Different k values
    @pytest.mark.parametrize("k_val", [1, 2, 3, 5, 8])
    def test_different_k_values(self, k_val):
        source = "design and analysis of algorithms divide and conquer dynamic programming greedy"
        suspect = "advanced design and analysis of algorithms divide and conquer graph theory"

        dc = run_divide_and_conquer(suspect, source, k=k_val)
        bf = run_brute_force(suspect, source, k=k_val)

        assert dc.similarity_percentage == bf.similarity_percentage
        assert dc.copied_word_count == bf.copied_word_count
        assert len(dc.matches) == len(bf.matches)
