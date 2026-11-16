# Plagiarism Evidence Finder — Project Demonstration Guide
## UPES Dehradun • DAA Problem 17

This guide outlines a polished 5-minute live demonstration flow for evaluators and professors.

---

## 1. Quick Launch

Launch the web dashboard:
```bash
streamlit run app.py
```
Or run the CLI interface:
```bash
python run_cli.py --reference
```

---

## 2. Recommended Demonstration Steps

### Step 1: UPES Reference Verification (Tab 2: Plagiarism Checker)
1. Select preset: **"UPES Reference Example (k=3, 73.33% Expected)"** from the sidebar dropdown.
2. Select algorithm mode: **"Both (Compare D&C vs Brute Force)"**.
3. Click **"🚀 Run Plagiarism Analysis"**.
4. Point out to the evaluator:
   - Similarity: exactly **73.33%**.
   - Suspect words: **15**, Copied words: **11**, Passages: **2**.
   - Parity between Divide & Conquer and Brute Force is identical.

### Step 2: Evidence Viewer & Highlighting (Tab 3: Evidence Viewer)
1. Switch to the **Evidence Viewer** tab.
2. Show side-by-side color-coded highlights:
   - **Passage #1:** *"the quick brown fox jumps over"* highlighted in Amber with label `[1..6]`.
   - **Passage #2:** *"dog near the river bank"* highlighted in Green with label `[9..13]`.
3. Highlight that original formatting, punctuation, and casing are preserved.

### Step 3: Head-to-Head Performance & Graphs (Tab 4: Algorithm Comparison)
1. Show the Head-to-Head table:
   - Compares Runtime, Word Comparisons, and Peak Memory.
2. Scroll to the **Empirical Scalability Charts**:
   - Point to the logarithmic runtime curve showing D&C outperforming Brute Force by over $100\times$ at 2,000 words.
   - Point to the word comparisons graph showing Brute Force doing $4,000,000+$ comparisons vs D&C doing only $2,356$.

### Step 4: 100,000+ Word Stress Test (Tab 5: Datasets & Benchmarks)
1. Switch to **Datasets & Benchmarks** tab.
2. Click **"🔥 Run Live 105,000-Word Stress Test"**.
3. Watch the progress spinner: in **~2 to 3 seconds**, the engine processes 105,000 words and identifies the plagiarized passages.
4. Explain that Brute Force on 105,000 words would take over 10 hours.

### Step 5: Academic Rigor & Theory (Tab 6: DAA Theory & Proof)
1. Show the inductive correctness proof and Master Theorem derivation ($T(n) = 2T(n/2) + O(k) \implies \Theta(n)$).
2. Open the expandable Viva Prep Q&A items to answer any questions from the evaluator.

---

## 3. Running Automated Tests Live

Show the professor that all 35 automated tests pass:
```bash
python -m pytest tests/ -v
```
All 35 unit and integration tests will execute and pass in ~3.3 seconds.
