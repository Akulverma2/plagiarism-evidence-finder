
# ⚡ Plagiarism Evidence Finder

> **A Divide and Conquer-based tool for finding exact copied word sequences between documents.**
>
> **Course:** Design and Analysis of Algorithms (DAA) — Problem 17  
> **University:** UPES, Dehradun

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Interface](https://img.shields.io/badge/Interface-Streamlit-indigo.svg)](https://streamlit.io/)
[![Main Algorithm](https://img.shields.io/badge/Main%20Algorithm-Divide%20%26%20Conquer-5267C5.svg)](#-algorithms)
[![Baseline](https://img.shields.io/badge/Baseline-Brute%20Force-D85B62.svg)](#2-brute-force-baseline)

---

## 🌟 Overview

The **Plagiarism Evidence Finder** compares a suspect document with a source document and identifies matching consecutive word sequences whose length is at least a user-selected minimum value, `k`.

The project demonstrates the **Divide and Conquer** design paradigm and compares its results with an independent **Brute Force** baseline. Instead of returning only a similarity score, it presents matching passages and their positions so users can inspect the evidence.

### ✨ Key Features

- **Divide and Conquer Algorithm:** Recursively examines sections of the suspect document and checks windows crossing each midpoint.
- **Brute Force Baseline:** Provides a straightforward comparison method for correctness and performance evaluation.
- **Evidence Highlighting:** Displays detected matching passages and their positions.
- **Similarity Score:** Calculates the proportion of suspect-document words covered by matching passages.
- **Document Input:** Supports text input and, where configured, `.txt`, `.pdf`, and `.docx` files.
- **Benchmarking:** Compares execution time and comparison counts across document sizes.
- **Academic Documentation:** Includes algorithm explanations, complexity discussion, test cases, and viva preparation material.

> **Scope:** This project detects exact matching word sequences after text normalization. It does not identify paraphrasing or conceptually similar writing.

---

## 🎯 UPES Reference Example

| Field | Content | Word Count |
|---|---|---:|
| **Source Document** | `the quick brown fox jumps over the lazy dog near the river bank` | 13 |
| **Suspect Document** | `yesterday the quick brown fox jumps over a sleeping dog near the river bank today` | 15 |
| **Minimum Sequence Length** | `k = 3` | — |

### Detected Evidence

| Passage | Matching Text | Suspect Positions | Source Positions | Words |
|---|---|---:|---:|---:|
| 1 | `the quick brown fox jumps over` | 1–6 | 0–5 | 6 |
| 2 | `dog near the river bank` | 9–13 | 8–12 | 5 |

Positions are zero-based and inclusive.

### Similarity Calculation

\[
\text{Similarity} =
\frac{\text{Unique Copied Suspect Words}}
{\text{Total Suspect Words}} \times 100
\]

\[
= \frac{6+5}{15}\times100 = 73.33\%
\]

The two detected passages cover 11 distinct suspect-document words out of 15.

---

## 🧠 Algorithms

### 1. Divide and Conquer — Main Algorithm

The main algorithm uses a source-document index and recursively processes ranges of the suspect document.

1. **Normalize and Tokenize:** Convert text into comparable tokens while retaining position information.
2. **Build Source Index:** Create a hash-based index of source-document windows containing `k` consecutive words.
3. **Divide:** Split the current suspect-document range at its midpoint.
4. **Solve Left and Right:** Recursively search for matches contained entirely within each half.
5. **Check Crossing Windows:** Examine windows that begin in the left half but extend across the midpoint.
6. **Verify Candidates:** Compare actual words to prevent hash collisions from producing false matches.
7. **Merge Intervals:** Combine overlapping or adjacent matching windows into maximal evidence passages.
8. **Calculate Similarity:** Count unique matched suspect-word positions to avoid double-counting overlapping evidence.

### 2. Brute Force — Baseline

The baseline checks each eligible suspect-document window against eligible source-document windows and verifies the words directly.

For `N` suspect words, `M` source words, and minimum window size `k`, a straightforward implementation has worst-case time complexity:

\[
O((N-k+1)(M-k+1)k) = O(NMk)
\]

This baseline helps validate the evidence produced by the main algorithm and compare measured performance.

### Complexity Note

The exact complexity of the Divide and Conquer implementation depends on the work performed at each recursive node, source-index representation, and candidate verification.

For the recursive crossing-window checks:

\[
T(N)=2T(N/2)+O(k)
\]

For fixed `k`, this recurrence is linear in `N`. Source-index construction and candidate-verification costs must also be included when reporting total complexity.

---

## 📊 Benchmarking

The project includes a benchmarking component intended to compare Divide and Conquer and Brute Force using the same input data.

Measurements include:

- Execution time
- Number of word comparisons
- Input document size
- Minimum window length `k`
- Speedup calculated from measured execution times

Only label a result as measured when it comes from an actual run on the stated machine and configuration. Mark extrapolated values as estimates.

---

## 🚀 Getting Started

### Requirements

- Python 3.10 or later
- Git
- Packages listed in `requirements.txt`

### 1. Clone the Repository

```bash
git clone https://github.com/Akulverma2/plagiarism-evidence-finder.git
cd plagiarism-evidence-finder
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Application

If `app.py` is present:

```bash
streamlit run app.py
```

Open the local URL printed in the terminal, usually:

`http://localhost:8501`

### 5. Run the CLI

If `run_cli.py` is included:

```bash
python run_cli.py --reference
```

For custom documents:

```bash
python run_cli.py --suspect path/to/suspect.txt --source path/to/source.txt -k 4 --algo both
```

### 6. Run Tests

If the repository includes a `tests/` directory:

```bash
python -m pytest tests/ -v
```

---

## 🧪 Important Test Scenarios

1. Empty source or suspect document
2. Documents shorter than `k`
3. Identical documents
4. Documents with no matching sequences
5. Repeated words
6. Multiple separate matching passages
7. Overlapping matching windows
8. Matches crossing recursive midpoints
9. Matches at the beginning or end of a document
10. Invalid or punctuation-only input
11. Different values of `k`
12. Large documents and stress-test inputs
13. Unreadable or unsupported files

---

## 📁 Project Structure

The following is a guide to the intended organization. Exact files may vary as development continues.

```text
plagiarism-evidence-finder/
├── app.py
├── run_cli.py
├── requirements.txt
├── README.md
├── DEVELOPMENT_LOG.md
├── src/
│   ├── algorithms/
│   │   ├── common.py
│   │   ├── divide_and_conquer.py
│   │   └── brute_force.py
│   ├── preprocessing/
│   │   ├── cleaner.py
│   │   └── file_reader.py
│   ├── evaluation/
│   │   └── benchmark.py
│   ├── datasets/
│   │   └── generator.py
│   └── visualizer/
│       ├── highlighter.py
│       └── charts.py
├── tests/
├── benchmarks/
├── assets/
├── data/
└── docs/
    ├── CORRECTNESS_PROOF.md
    ├── COMPLEXITY_ANALYSIS.md
    ├── DEMO_GUIDE.md
    └── VIVA_GUIDE.md
```

---

## 👥 Team Members

**Submitted to:** Prof. Priyabrata Dash  
**Course:** Design and Analysis of Algorithms (DAA)  
**University:** UPES, Dehradun

| S. No. | Team Member | SAP ID | Batch |
|---:|---|---:|---|
| 1 | Granth | 590025276 | B1 |
| 2 | Nimisha | 590029380 | B2 |
| 3 | Akul Verma | 590022505 | B2 |
| 4 | Bankim | 590027520 | B2 |
| 5 | Bharat | 590021893 | B2 |
| 6 | Vivan | 590029475 | B2 |

### Contribution Breakdown

| Team Member | Contribution |
|---|---|
| **Granth** | Core Divide and Conquer algorithm, pseudocode, and correctness argument |
| **Nimisha** | Hand-verified reference example, edge cases, stress tests, and invalid-input tests |
| **Akul Verma** | User interface/dashboard, highlighted evidence output, and live demonstration |
| **Bankim** | Performance-comparison plots using benchmark results |
| **Bharat** | Small, medium, and large datasets; data-cleaning rules; and ground-truth answers |
| **Vivan** | Brute Force baseline and benchmarking code |

---

## 📚 Academic Documentation

Refer to these documents if included in the repository:

- **Correctness Proof:** `docs/CORRECTNESS_PROOF.md`
- **Complexity Analysis:** `docs/COMPLEXITY_ANALYSIS.md`
- **Viva Guide:** `docs/VIVA_GUIDE.md`
- **Demonstration Guide:** `docs/DEMO_GUIDE.md`

---

## ⚠️ Limitations

- Detects exact word-sequence matches after normalization.
- Does not establish intent or determine whether a match is plagiarism; it provides textual evidence for human review.
- Paraphrased passages and semantic similarity are outside the current scope.
- Similarity depends on the chosen `k`, tokenization, normalization, and interval-merging rules.
- Benchmark results depend on hardware, dataset, and system load.

---

## 🎓 Academic Credits

Developed as a Design and Analysis of Algorithms (DAA) project at **UPES, Dehradun**.

**Submitted to:** Prof. Priyabrata Dash

---

## 📌 Project Status

This repository is an academic DAA project. Refer to the source code and repository files for the latest implementation details, supported formats, test results, and benchmark measurements.
