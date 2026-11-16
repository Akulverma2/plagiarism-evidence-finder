"""Synthetic Dataset Generator for DAA Plagiarism Evidence Finder.

Generates:
1. Small Dataset:
   - Reference UPES sample (15 words, 73.33% similarity)
   - Academic abstract pairs (~100-200 words)
2. Medium Dataset:
   - 50 documents of ~2,000 words each with controlled plagiarism rates (0% to 100%)
   - Ground truth catalog saved as JSON and CSV
3. Large Dataset:
   - Massive 100,000+ words suspect and source document pair for stress testing
"""

import os
import json
import random
from typing import List, Dict, Any, Tuple


VOCABULARY = [
    "algorithm", "divide", "conquer", "recursion", "recurrence", "complexity",
    "asymptotic", "optimization", "dynamic", "programming", "greedy", "graph",
    "tree", "binary", "search", "sorting", "quicksort", "mergesort", "heapsort",
    "matrix", "multiplication", "strassen", "master", "theorem", "logarithmic",
    "polynomial", "exponential", "linear", "quadratic", "structure", "pointer",
    "hash", "table", "collision", "resolution", "probing", "chaining", "vertex",
    "edge", "directed", "acyclic", "topological", "traversal", "breadth", "depth",
    "shortest", "path", "dijkstra", "bellman", "ford", "floyd", "warshall",
    "minimum", "spanning", "kruskal", "prim", "disjoint", "union", "find",
    "network", "flow", "ford", "fulkerson", "bipartite", "matching", "np",
    "complete", "reduction", "sat", "clique", "vertex", "cover", "approximation",
    "randomized", "amortized", "potential", "accounting", "splay", "avl",
    "red", "black", "b", "tree", "trie", "suffix", "automaton", "kmp",
    "rabin", "karp", "boyer", "moore", "interval", "scheduling", "knapsack",
    "fibonacci", "memoization", "bottom", "up", "top", "down", "subproblem"
]


def generate_natural_text(word_count: int, seed: int = 42) -> str:
    """Generate realistic academic prose by chaining words with standard sentence structure."""
    rng = random.Random(seed)
    words = []
    current_sentence_len = rng.randint(8, 16)
    
    for i in range(word_count):
        word = rng.choice(VOCABULARY)
        if len(words) == 0 or words[-1].endswith("."):
            word = word.capitalize()
            
        current_sentence_len -= 1
        if current_sentence_len <= 0 and i < word_count - 1:
            words.append(word + ".")
            current_sentence_len = rng.randint(8, 16)
        else:
            words.append(word)
            
    if not words[-1].endswith("."):
        words[-1] += "."
        
    return " ".join(words)


def create_plagiarized_pair(
    base_text: str,
    target_similarity_pct: float,
    seed: int = 100
) -> Tuple[str, str, Dict[str, Any]]:
    """Create a (source, suspect) pair with a known target plagiarism percentage.
    
    In-place copies contiguous chunks from source into suspect.
    """
    rng = random.Random(seed)
    source_words = base_text.split()
    total_words = len(source_words)
    
    words_to_copy = int(total_words * (target_similarity_pct / 100.0))
    
    # Generate unique non-matching suspect text
    suspect_base = generate_natural_text(total_words, seed=seed + 9999).split()
    
    injected_passages = []
    copied_so_far = 0
    
    # Inject 1 to 5 chunks of contiguous passages
    chunk_count = rng.randint(1, 4) if words_to_copy > 20 else 1
    chunk_size = words_to_copy // chunk_count if chunk_count > 0 else 0
    
    for c in range(chunk_count):
        if copied_so_far >= words_to_copy:
            break
        actual_chunk = min(chunk_size, words_to_copy - copied_so_far)
        if actual_chunk < 3:
            actual_chunk = words_to_copy - copied_so_far
        if actual_chunk <= 0:
            break
            
        src_pos = rng.randint(0, max(0, total_words - actual_chunk))
        susc_pos = rng.randint(0, max(0, len(suspect_base) - actual_chunk))
        
        # Copy chunk
        chunk = source_words[src_pos : src_pos + actual_chunk]
        suspect_base[susc_pos : susc_pos + actual_chunk] = chunk
        
        injected_passages.append({
            "source_start": src_pos,
            "source_end": src_pos + actual_chunk - 1,
            "suspect_start": susc_pos,
            "suspect_end": susc_pos + actual_chunk - 1,
            "length": actual_chunk
        })
        copied_so_far += actual_chunk

    suspect_text = " ".join(suspect_base)
    source_text = " ".join(source_words)
    
    metadata = {
        "target_similarity_pct": target_similarity_pct,
        "words_to_copy": words_to_copy,
        "injected_passages": injected_passages,
        "total_source_words": len(source_words),
        "total_suspect_words": len(suspect_base)
    }
    return source_text, suspect_text, metadata


def generate_all_datasets(base_dir: str = "data"):
    """Generate and store small, medium (50 docs), and large (100k+ words) datasets."""
    small_dir = os.path.join(base_dir, "small")
    medium_dir = os.path.join(base_dir, "medium")
    large_dir = os.path.join(base_dir, "large")

    os.makedirs(small_dir, exist_ok=True)
    os.makedirs(medium_dir, exist_ok=True)
    os.makedirs(large_dir, exist_ok=True)

    # 1. SMALL DATASETS
    # Reference UPES pair
    upes_source = "the quick brown fox jumps over the lazy dog near the river bank"
    upes_suspect = "yesterday the quick brown fox jumps over a sleeping dog near the river bank today"
    with open(os.path.join(small_dir, "upes_reference_source.txt"), "w", encoding="utf-8") as f:
        f.write(upes_source)
    with open(os.path.join(small_dir, "upes_reference_suspect.txt"), "w", encoding="utf-8") as f:
        f.write(upes_suspect)

    # Short academic excerpt (approx 150 words)
    short_source = generate_natural_text(150, seed=123)
    _, short_suspect, _ = create_plagiarized_pair(short_source, 45.0, seed=124)
    with open(os.path.join(small_dir, "academic_source.txt"), "w", encoding="utf-8") as f:
        f.write(short_source)
    with open(os.path.join(small_dir, "academic_suspect.txt"), "w", encoding="utf-8") as f:
        f.write(short_suspect)

    # 2. MEDIUM DATASET (~50 documents of ~2,000 words each)
    medium_catalog = []
    # Generate 25 source documents and 25 paired suspect documents with varying plagiarism rates
    for i in range(1, 26):
        src_text = generate_natural_text(2000, seed=1000 + i)
        sim_pct = round(random.Random(2000 + i).uniform(10.0, 90.0), 2)
        _, susc_text, meta = create_plagiarized_pair(src_text, sim_pct, seed=3000 + i)

        src_filename = f"doc_{i:02d}_source.txt"
        susc_filename = f"doc_{i:02d}_suspect.txt"

        with open(os.path.join(medium_dir, src_filename), "w", encoding="utf-8") as f:
            f.write(src_text)
        with open(os.path.join(medium_dir, susc_filename), "w", encoding="utf-8") as f:
            f.write(susc_text)

        medium_catalog.append({
            "pair_id": i,
            "source_file": src_filename,
            "suspect_file": susc_filename,
            "approx_words": 2000,
            "target_similarity_pct": sim_pct,
            "injected_passages": len(meta["injected_passages"])
        })

    with open(os.path.join(medium_dir, "dataset_catalog.json"), "w", encoding="utf-8") as f:
        json.dump(medium_catalog, f, indent=2)

    # 3. LARGE DATASET (Suspect document containing at least 100,000 words)
    print("Generating large dataset (>= 100,000 words)...")
    large_words_count = 105000  # Exceeds 100,000 word specification
    large_source = generate_natural_text(large_words_count, seed=777)
    _, large_suspect, large_meta = create_plagiarized_pair(large_source, 35.0, seed=888)

    with open(os.path.join(large_dir, "large_source_105k.txt"), "w", encoding="utf-8") as f:
        f.write(large_source)
    with open(os.path.join(large_dir, "large_suspect_105k.txt"), "w", encoding="utf-8") as f:
        f.write(large_suspect)

    with open(os.path.join(large_dir, "large_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(large_meta, f, indent=2)

    print("All datasets generated successfully:")
    print(f"- Small: {small_dir}")
    print(f"- Medium (50 docs): {medium_dir}")
    print(f"- Large (>=100k words): {large_dir}")


if __name__ == "__main__":
    generate_all_datasets()
