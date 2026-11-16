# ⚡ Plagiarism Evidence Finder
> **Autonomous Algorithmic Plagiarism Detection with Exact Word-Sequence Verification**  
> **Course:** Design and Analysis of Algorithms (DAA) — Problem 17  
> **University:** UPES, Dehradun  

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/Interface-Streamlit%20SaaS-indigo.svg)](https://streamlit.io/)
[![Algorithm](https://img.shields.io/badge/Core%20Algorithm-Divide%20%26%20Conquer%20%28O%28N%20log%20N%29%29-5267C5.svg)](#-algorithms-implemented)
[![Baseline](https://img.shields.io/badge/Baseline-Brute%20Force%20%28O%28N%C2%B7M%C2%B7k%29%29-D85B62.svg)](#2-brute-force-baseline-algorithm)
[![Tests](https://img.shields.io/badge/Test%20Suite-35%2F35%20Passed%20%E2%9C%93-238B68.svg)](tests/)
[![Stress Test](https://img.shields.io/badge/Stress%20Scale-105%2C000%2B%20Words-success.svg)](data/large/)

---

## 🌟 Overview

The **Plagiarism Evidence Finder** is an academic-grade, enterprise-styled plagiarism detection engine built for the **Design and Analysis of Algorithms (DAA)** curriculum at **UPES, Dehradun**. The system compares a suspect document against an original source document to identify copied word sequences of minimum length $k$.

### ✨ Key Features
- **Divide & Conquer Core Paradigm:** Hierarchically subdivides document word sequences while rigorously accounting for recursive midpoint crossing boundaries without omission or double-counting.
- **Brute Force Baseline:** Provides an independent nested-comparison baseline tracking every word equality check to compute empirical speedup factors.
- **SaaS-Grade Modern UI:** Modern interface inspired by Linear and Notion with side-by-side color-coded evidence highlights, coordinate badges (`#1`, `#2`), and hover tooltips.
- **Empirical Scalability:** Verified on corpora ranging from 50 words up to **105,000+ words** in **~2.1 seconds**.
- **Universal Document Ingestion:** Supports `.txt`, `.pdf` (with PyMuPDF / pdfplumber fallback), and `.docx` (python-docx) with safe error reporting.
- **Comprehensive Academic Suite:** Includes strong mathematical induction correctness proofs, Master Theorem derivations, and oral examination viva preparation guides.

---

## 🎯 Mandatory UPES Reference Example Verification

The UPES course syllabus defines a mandatory reference test case:

| Field | Text Content | Length |
|---|---|---|
| **Source Document** | `the quick brown fox jumps over the lazy dog near the river bank` | 13 words |
| **Suspect Document** | `yesterday the quick brown fox jumps over a sleeping dog near the river bank today` | 15 words |
| **Window Size ($k$)** | $k = 3$ consecutive words | — |

### Identified Evidence Passages:
1. **Passage #1:** `"the quick brown fox jumps over"`  
   - **Suspect Positions:** `[1 .. 6]` (Length: 6 words)  
   - **Source Positions:** `[0 .. 5]`
2. **Passage #2:** `"dog near the river bank"`  
   - **Suspect Positions:** `[9 .. 13]` (Length: 5 words)  
   - **Source Positions:** `[8 .. 12]`

### Similarity Metric:
$$\text{Similarity} = \frac{\text{Copied Suspect Words}}{\text{Total Suspect Words}} \times 100 = \frac{6 + 5}{15} \times 100 = \mathbf{73.33\%}$$

Both **Divide and Conquer** and **Brute Force** algorithms yield 100% identical evidence, verified in automated test `tests/test_reference.py`.

---

## 📂 Project Architecture

```
plagiarism-evidence-finder/
├── app.py                             # Modern Streamlit SaaS Application
├── run_cli.py                         # Head-to-Head CLI Analysis Tool
├── requirements.txt                   # Production Dependencies
├── DEVELOPMENT_LOG.md                 # Complete Autonomous Engineering Audit Log
├── README.md                          # Project Documentation
├── src/
│   ├── algorithms/
│   │   ├── common.py                  # Token, MatchInterval, EvidenceResult classes
│   │   ├── divide_and_conquer.py      # Divide & Conquer algorithm & crossing logic
│   │   └── brute_force.py             # Brute Force baseline algorithm
│   ├── preprocessing/
│   │   ├── cleaner.py                 # Normalization, tokenization, coordinate mapping
│   │   └── file_reader.py             # Universal loader (TXT, PDF, DOCX)
│   ├── evaluation/
│   │   └── benchmark.py               # Empirical benchmarking engine
│   ├── datasets/
│   │   └── generator.py               # Small, Medium (50 docs), and Large (105k) generator
│   └── visualizer/
│       ├── highlighter.py             # Pastel HTML text highlighter with badges
│       └── charts.py                  # Publication Matplotlib plot generators
├── tests/
│   ├── test_reference.py              # Mandatory UPES reference test (73.33%)
│   ├── test_edge_cases.py             # 15 mandatory edge case tests
│   ├── test_cleaner.py                # Preprocessing and token coordinate tests
│   ├── test_similarity.py             # Interval merging and union calculations
│   ├── test_file_reader.py            # File format parsing tests
│   └── test_stress.py                 # 105,000-word stress test
├── benchmarks/
│   ├── scaling_benchmark.csv          # Real empirical scaling data (50 to 100k words)
│   └── k_sensitivity.json             # Empirical window size k sensitivity data
├── assets/charts/                     # Exported Matplotlib plots
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
   - **Base Case ($L < k$):** Returns $\emptyset$.
   - **Base Case ($L = k$):** Evaluates the single window against the source index.
   - **Left Subproblem:** Recursively identifies matches completely in $[L, M)$.
   - **Right Subproblem:** Recursively identifies matches completely in $[M, R)$.
   - **Crossing Midpoint:** Checks all windows starting in:
     $$i \in [\max(L, M - k + 1), \, \min(R - k, M - 1)]$$
4. **Collision Verification:** Verifies candidate matches word-by-word via `verify_window_match()` to eliminate false positives from hash collisions.
5. **Interval Merging:** Merges overlapping and contiguous matching windows into maximal copied passages.
6. **Similarity Calculation:**
   $$\text{Similarity} = \left(\frac{\text{Unique Copied Suspect Words}}{\text{Total Suspect Words}}\right) \times 100$$

### 2. Brute Force (Baseline Algorithm)
- Directly checks all $(N - k + 1)$ suspect windows against all $(M - k + 1)$ source windows.
- Counts every individual word comparison operation.
- Time Complexity: $O(N \cdot M \cdot k)$.

---

## 📊 Empirical Benchmarks (Verified Local Measurements)

Measurements recorded on local Windows 11 hardware across sizes from 50 to 100,000 words:

| Document Size (Words) | Divide & Conquer Time | D&C Word Comparisons | Brute Force Time | Brute Force Comparisons | D&C Speedup |
|---|---|---|---|---|---|
| **50** | 0.0014 s | 48 | 0.0028 s | 2,275 | **2.0x** |
| **250** | 0.0041 s | 224 | 0.0252 s | 61,839 | **6.1x** |
| **1,000** | 0.0176 s | 984 | 1.0245 s | 1,005,365 | **58.2x** |
| **2,000** | **0.0357 s** | **2,356** | **4.0437 s** | **4,032,042** | **113.3x** |
| **10,000** | 0.3037 s | 11,968 | *(est. ~100 s)* | *(est. ~100M)* | **> 300x** |
| **100,000** | **2.1121 s** | **120,480** | *(est. ~10 hours)* | *(est. ~40 Billion)* | **> 15,000x** |

---

## 🚀 Quick Start Guide

### 1. Requirements & Setup
Make sure Python 3.10+ is installed:
```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit GUI
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 3. Run via Command-Line Interface (CLI)
Run the UPES reference test:
```bash
python run_cli.py --reference
```
Or analyze custom files:
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
14. Scalability sanity (1,000 words)
15. Different $k$ values ($k \in \{1, 2, 3, 5, 8\}$)
16. Massive 105,000+ words stress test

---

## 📚 Academic Documentation
- **[Mathematical Correctness Proof](docs/CORRECTNESS_PROOF.md)**: Strong mathematical induction proof showing base cases, recursive cases, crossing window bounds, interval merging, and union similarity calculation.
- **[Complexity Analysis & PBL Audit](docs/COMPLEXITY_ANALYSIS.md)**: Master Theorem analysis ($T(n) = 2T(n/2) + O(k) \implies \Theta(n)$), PBL complexity audit, and theoretical vs measured performance comparisons.
- **[DAA Viva Guide](docs/VIVA_GUIDE.md)**: High-yield oral questions and model answers for evaluation.
- **[Demonstration Guide](docs/DEMO_GUIDE.md)**: Step-by-step 5-minute evaluator demonstration guide.

---

## 🎓 Academic Credits & Attribution
- **Institution:** University of Petroleum and Energy Studies (UPES), Dehradun
- **Course:** Design and Analysis of Algorithms (DAA)
- **Problem:** 17 — Plagiarism Evidence Finder using Divide and Conquer
- **Author / Repository Owner:** [Akulverma2](https://github.com/Akulverma2)
