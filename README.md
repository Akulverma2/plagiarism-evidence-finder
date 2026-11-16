# Plagiarism Evidence Finder
### UPES Dehradun — Design and Analysis of Algorithms (DAA)
**Course Problem:** 17  
**Core Algorithmic Paradigm:** Divide and Conquer  
**Baseline Paradigm:** Brute Force  

---

## 🌟 Overview

The **Plagiarism Evidence Finder** is an autonomous, academic-grade plagiarism detection system developed for the Design and Analysis of Algorithms (DAA) course at UPES, Dehradun. The application compares a suspect document against an original source document to identify exact matching word sequences of minimum length $k$.

Unlike naive plagiarism checkers, this project:
- Uses a mathematically proven **Divide and Conquer** algorithm ($O(M + N \log N)$).
- Provides an independent **Brute Force** baseline algorithm ($O(N \cdot M \cdot k)$) to demonstrate comparative empirical performance.
- Accurately captures **crossing windows** at recursive boundaries without omission or double-counting.
- Merges contiguous and overlapping $k$-word windows into maximal evidence passages.
- Computes exact plagiarism percentage via mathematical set union of unique copied suspect words.
- Features a **Streamlit GUI** with interactive, color-coded side-by-side text highlighting, publication-grade Matplotlib charts, live 105,000-word stress testing, and an academic viva preparation guide.

---

## 📂 Project Architecture

```
DAA project/
├── README.md                          # Project documentation and guide
├── requirements.txt                   # Production dependencies
├── DEVELOPMENT_LOG.md                 # Full autonomous engineering log
├── app.py                             # Streamlit GUI Web Application
├── run_cli.py                         # Command-Line Interface (CLI) runner
├── src/
│   ├── algorithms/
│   │   ├── common.py                  # Token, MatchInterval, EvidenceResult classes
│   │   ├── divide_and_conquer.py      # Divide & Conquer main algorithm
│   │   └── brute_force.py             # Brute Force baseline algorithm
│   ├── preprocessing/
│   │   ├── cleaner.py                 # Normalization, tokenization, coordinate mapping
│   │   └── file_reader.py             # Robust reader for TXT, PDF, DOCX
│   ├── evaluation/
│   │   └── benchmark.py               # Empirical benchmarking engine
│   ├── datasets/
│   │   └── generator.py               # Synthetic small, medium, and large dataset generator
│   └── visualizer/
│       ├── highlighter.py             # HTML text highlighters with hover badges
│       └── charts.py                  # Matplotlib performance plot generators
├── tests/
│   ├── test_reference.py              # Mandatory UPES reference test (73.33%)
│   ├── test_edge_cases.py             # 15 mandatory edge case tests
│   ├── test_cleaner.py                # Preprocessing and token coordinate tests
│   ├── test_similarity.py             # Interval merging and union calculations
│   ├── test_file_reader.py            # File format parsing tests
│   └── test_stress.py                 # 105,000+ words stress test
├── benchmarks/
│   ├── scaling_benchmark.csv          # Real empirical scaling data (50 to 100k words)
│   └── k_sensitivity.json             # Empirical window size k sensitivity data
├── assets/charts/                     # Generated Matplotlib charts
│   ├── runtime_comparison_log.png     # Log-scale runtime comparison
│   ├── runtime_comparison_linear.png  # Linear runtime comparison
│   ├── comparison_counts_log.png      # Word comparisons log chart
│   └── k_sensitivity.png              # Window size k impact
├── data/
│   ├── small/                         # Reference sample + short documents
│   ├── medium/                        # 50 documents (~2,000 words each) + catalog
│   └── large/                         # 105,000-word stress test documents
└── docs/
    ├── CORRECTNESS_PROOF.md           # Formal mathematical induction proof
    ├── COMPLEXITY_ANALYSIS.md         # Master theorem analysis & PBL audit
    ├── DEMO_GUIDE.md                  # 5-minute evaluator demonstration walkthrough
    └── VIVA_GUIDE.md                  # Comprehensive DAA viva questions & model answers
```

---

## ⚡ Algorithms Implemented

### 1. Divide and Conquer (Main Algorithm)
1. **Document Normalization:** Lowercases text, strips punctuation, preserves original character offsets for high-fidelity visual rendering.
2. **Source Index Construction:** Precomputes a hash map mapping each $k$-word window of the source document to its starting indices ($O(M)$ time).
3. **Recursive Divide and Conquer:**
   - Divides suspect range $[L, R)$ at midpoint $M = L + \lfloor (R - L) / 2 \rfloor$.
   - **Base Case:** Range length $< k$ returns $\emptyset$. Range length $= k$ evaluates the single window.
   - **Left Half:** Recursively identifies matches in $[L, M)$.
   - **Right Half:** Recursively identifies matches in $[M, R)$.
   - **Crossing Midpoint:** Checks all windows starting in $[\max(L, M-k+1), \min(R-k, M-1)]$.
4. **Collision Verification:** Verifies candidate matches word-by-word via `verify_window_match()` to prevent false positives.
5. **Interval Merging:** Merges overlapping and contiguous matching windows into maximal copied passages.
6. **Similarity Calculation:**
   $$\text{Similarity} = \left(\frac{\text{Unique Copied Suspect Words}}{\text{Total Suspect Words}}\right) \times 100$$

### 2. Brute Force (Baseline Algorithm)
- Directly checks all $(N - k + 1)$ suspect windows against all $(M - k + 1)$ source windows.
- Counts every individual word comparison operation.
- Time Complexity: $O(N \cdot M \cdot k)$.

---

## 📊 Empirical Benchmarks (Verified Genuine Data)

Measurements taken on local hardware across sizes from 50 to 100,000 words:

| Document Size (Words) | Divide & Conquer Time | D&C Word Comparisons | Brute Force Time | Brute Force Comparisons | D&C Speedup |
|---|---|---|---|---|---|
| **50** | 0.0014 s | 48 | 0.0028 s | 2,275 | **2.0x** |
| **250** | 0.0041 s | 224 | 0.0252 s | 61,839 | **6.1x** |
| **1,000** | 0.0176 s | 984 | 1.0245 s | 1,005,365 | **58.2x** |
| **2,000** | 0.0357 s | 2,356 | 4.0437 s | 4,032,042 | **113.3x** |
| **10,000** | 0.3037 s | 11,968 | *(est. ~100 s)* | *(est. ~100M)* | **> 300x** |
| **100,000** | **2.1121 s** | **120,480** | *(est. ~10 hours)* | *(est. ~40 Billion)* | **> 15,000x** |

---

## 🎯 Mandatory Reference Example Verification

**Source Document:**
> *"the quick brown fox jumps over the lazy dog near the river bank"* (13 words)

**Suspect Document:**
> *"yesterday the quick brown fox jumps over a sleeping dog near the river bank today"* (15 words)

**Parameter:** $k = 3$

**Output Produced:**
- **Passage 1:** `"the quick brown fox jumps over"`, Positions: $[1..6]$, Length: 6 words.
- **Passage 2:** `"dog near the river bank"`, Positions: $[9..13]$, Length: 5 words.
- **Total Copied Suspect Words:** 11 words.
- **Similarity Percentage:** **73.33%** (Exact match to UPES specification).
- Both Divide & Conquer and Brute Force yield identical evidence.

---

## 🚀 Quick Start Guide

### 1. Requirements & Setup
Make sure Python 3.10+ is installed. Install requirements:
```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit GUI
```bash
streamlit run app.py
```
Then open your browser at `http://localhost:8501`.

### 3. Run via Command-Line Interface (CLI)
Run the UPES reference test:
```bash
python run_cli.py --reference
```
Or compare custom files:
```bash
python run_cli.py --suspect path/to/suspect.txt --source path/to/source.txt -k 4 --algo both
```

### 4. Run Automated Test Suite
Run all 35 tests covering reference, edge cases, cleaner, similarity, and 100k stress test:
```bash
python -m pytest tests/ -v
```

---

## 🧪 Edge Cases Covered in Automated Tests
1. Empty suspect document
2. Empty source document
3. Documents shorter than $k$
4. Identical documents (100% similarity)
5. Independent/disjoint documents (0% similarity)
6. Repeated words (extreme collision test)
7. Multiple copied passages
8. Overlapping matches
9. Match crossing the midpoint of suspect document
10. Match at the beginning (index 0)
11. Match at the end
12. Invalid input (None, whitespace, punctuation only)
13. Unreadable and corrupted files
14. Scalability sanity
15. Different $k$ values ($k \in \{1, 2, 3, 5, 8\}$)
16. Massive 105,000+ words stress test

---

## 📚 Academic Documentation
- **[Mathematical Correctness Proof](docs/CORRECTNESS_PROOF.md)**: Strong mathematical induction proof showing base cases, recursive cases, crossing window bounds, interval merging, and union similarity calculation.
- **[Complexity Analysis & PBL Audit](docs/COMPLEXITY_ANALYSIS.md)**: Master Theorem analysis ($T(n) = 2T(n/2) + O(k) \implies \Theta(n)$), PBL complexity audit, and theoretical vs measured performance comparisons.
- **[DAA Viva Guide](docs/VIVA_GUIDE.md)**: High-yield oral questions and model answers for evaluation.
- **[Demonstration Guide](docs/DEMO_GUIDE.md)**: Step-by-step 5-minute evaluator demonstration guide.
