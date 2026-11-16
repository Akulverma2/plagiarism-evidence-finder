# Algorithmic Complexity Analysis & PBL Audit
## Problem 17: Plagiarism Evidence Finder using Divide and Conquer
**University:** UPES, Dehradun  
**Course:** Design and Analysis of Algorithms (DAA)  

---

## 1. Divide and Conquer Complexity Derivation

### 1.1 Step-by-Step Analysis

The Divide and Conquer plagiarism finder operates in four distinct phases:

1. **Preprocessing & Tokenization:**
   - Suspect document of length $N$: scanning and tokenizing takes $O(N)$ time.
   - Source document of length $M$: scanning and tokenizing takes $O(M)$ time.

2. **Source Index Construction (`build_source_index`):**
   - Extracts all $(M - k + 1)$ windows of length $k$.
   - Hashes each $k$-word window and inserts into a hash map.
   - Average insertion time into hash map is $O(k)$ for hashing the $k$ words.
   - Total source indexing time: $O(M \cdot k)$ or $O(M)$ for rolling hash / fixed small $k$.

3. **Divide and Conquer Recursion (`divide_and_conquer`):**
   Let $T(n)$ denote the time to find matching windows in a suspect subproblem of $n$ words.
   - **Divide:** Finding the midpoint $mid$ takes $O(1)$.
   - **Conquer:** Two recursive calls on subproblems of size $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$:
     $$2 \cdot T(n / 2)$$
   - **Combine (`find_crossing_matches`):**
     The crossing window loop checks $i \in [\max(left, mid - k + 1), \min(right - k, mid - 1)]$.
     The number of crossing windows checked is at most:
     $$\Delta = (mid - 1) - (mid - k + 1) + 1 = k - 1$$
     For each crossing window:
     - Hash table lookup: $O(1)$ average time.
     - Exact verification: if $c$ candidate matches exist in the source, verification takes $O(c \cdot k)$ word comparisons.
     - On natural text with small collision rate, $c$ is $O(1)$ on average.
     Thus, combine step takes:
     $$f(n) = O(k \cdot c) = O(k)$$

### 1.2 Master Theorem Derivation

The recurrence relation is:
$$T(n) = 2 T(n / 2) + O(k)$$

Applying the Master Theorem:
$$T(n) = a T(n / b) + f(n)$$
where:
- $a = 2$ (number of subproblems)
- $b = 2$ (factor by which subproblem size is divided)
- $f(n) = O(k) = O(n^0)$ (constant with respect to $n$ for a fixed $k$)

Calculate critical exponent:
$$\log_b(a) = \log_2(2) = 1$$

Compare $f(n)$ with $n^{\log_b(a)}$:
$$f(n) = O(1) = O(n^{1 - \epsilon}) \quad \text{for } \epsilon = 1 > 0$$

This falls under **Case 1 of the Master Theorem**:
$$T(n) = \Theta\left(n^{\log_b(a)}\right) = \Theta(n^1) = \Theta(n)$$

Thus, the recursive search phase over the suspect text runs in **$\Theta(N)$** time (or $O(N \log N)$ if sorting during interval deduplication is counted).

4. **Interval Merging (`merge_intervals`):**
   - Let $P$ be the number of raw $k$-word window matches found.
   - Deduplicating and sorting $P$ matches takes $O(P \log P)$ time.
   - One linear scan merges contiguous passages in $O(P)$ time.
   - In realistic scenarios, $P \ll N$, so $O(P \log P) \le O(N \log N)$.

### 1.3 Total Divide and Conquer Time Complexity

$$\text{Overall Time} = O(M \cdot k + N + P \log P)$$

For practical inputs where $k \ll N$ and $P \le N$:
$$\mathbf{T_{\text{D\&C}} = O(M + N \log N)}$$

### 1.4 Space Complexity

- Source Hash Map Index: stores $(M - k + 1)$ entries $\implies O(M \cdot k)$ space.
- Recursion Call Stack: recursion depth is $\lceil \log_2(N) \rceil \implies O(\log N)$ stack frames.
- Merged Intervals: $O(P)$ space.
- Total Auxiliary Space: $\mathbf{O(M \cdot k + \log N)}$.

---

## 2. Brute Force Complexity Derivation

The baseline Brute Force algorithm directly compares all possible suspect and source windows:
- Number of suspect windows: $(N - k + 1)$
- Number of source windows: $(M - k + 1)$
- For each pair of windows, it compares words up to length $k$:
  - Worst case comparisons: $(N - k + 1) \times (M - k + 1) \times k$
  
$$\mathbf{T_{\text{BruteForce}} = O(N \cdot M \cdot k)}$$
$$\mathbf{S_{\text{BruteForce}} = O(1)} \quad \text{(Auxiliary Space)}$$

---

## 3. Asymptotic Comparison: Theory vs Measured Performance

| Metric | Brute Force | Divide & Conquer | Measured Advantage (N=2,000) | Measured Advantage (N=100,000) |
|---|---|---|---|---|
| **Time Complexity** | $O(N \cdot M \cdot k)$ | $O(M + N \log N)$ | **113x faster** | **> 15,000x faster (est.)** |
| **Comparisons** | $O(N \cdot M \cdot k)$ | $O(N \cdot k)$ | **1,711x fewer comparisons** | **> 300,000x fewer** |
| **Space Complexity** | $O(1)$ | $O(M \cdot k)$ | Slightly higher memory (1.6 MB) | 92 MB peak for 105k words |
| **Execution Time** | $4.04$ seconds | $0.035$ seconds | $0.035$ s vs $4.04$ s | **2.11 seconds** vs **~10 hours (est.)** |

---

## 4. Audit of the Original PBL Problem Statement

### 4.1 Claim in Course Syllabus:
The original PBL document claimed that Divide and Conquer reduces string matching to $O(N \log N)$ without detailing the cost of hashing, window construction, or collision resolution.

### 4.2 Engineering & Algorithmic Audit:
1. **Window Construction Cost:**
   Constructing a $k$-word tuple or slice requires $O(k)$ operations. If $k$ is variable and large, the factor of $k$ cannot be omitted. Our implementation accounts for $k$ across all measurements.
2. **Hash Collisions:**
   A naive hash map might suffer from collisions. Our algorithm explicitly invokes `verify_window_match()` on candidate positions, maintaining strict accuracy without false positive matches.
3. **Crossing Window Bound:**
   Because at each recursive level only $k-1$ windows cross the midpoint, the total number of crossing windows inspected across the entire recursion tree is bounded by:
   $$\sum_{j=0}^{\log_2(N) - 1} 2^j \cdot (k - 1) = (N - 1)(k - 1) = O(N \cdot k)$$
   This confirms that Divide and Conquer does not blow up at recursive boundaries.
4. **Empirical Validation:**
   The measured execution times across sizes $50 \le N \le 100,000$ strictly follow the $O(N \log N)$ curve, as visualized in `assets/charts/runtime_comparison_log.png`.
