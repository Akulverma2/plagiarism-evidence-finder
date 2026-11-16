# UPES DAA Viva & Oral Examination Guide
## Problem 17: Plagiarism Evidence Finder using Divide and Conquer
**Course:** Design and Analysis of Algorithms (DAA)  
**Institution:** UPES, Dehradun  

---

## High-Yield Viva Questions and Model Answers

### Q1: What is the core algorithmic problem being solved?
**Answer:** The project addresses the problem of detecting copied word sequences of length $\ge k$ between a suspect document and an original/source document, reporting exact word coordinates, length of copied passages, overall plagiarism percentage, and visual evidence highlights.

---

### Q2: Why is Divide and Conquer chosen for this problem?
**Answer:** 
1. **Hierarchical Partitioning:** By recursively dividing the suspect document into left and right halves, we reduce the search space into independent subproblems.
2. **Boundary Disjointness:** Every $k$-word window either lies completely in the left half, completely in the right half, or crosses the midpoint. This partition is mutually exclusive and exhaustive.
3. **Complexity Reduction:** Combined with a precomputed source hash index ($O(M)$), the search runs in $O(N \log N)$ rather than the $O(N \cdot M \cdot k)$ required by Brute Force.
4. **Parallelizability:** Subproblems on the left and right halves can be executed concurrently on multi-threaded or distributed systems.

---

### Q3: How do you handle windows that cross the midpoint?
**Answer:**
A $k$-word window starting at suspect index $i$ spans $[i, i + k - 1]$.
For the window to cross the midpoint $M = \lfloor (L + R)/2 \rfloor$, it must:
- Start strictly before $M$: $i < M \iff i \le M - 1$
- End at or after $M$: $i + k - 1 \ge M \iff i \ge M - k + 1$

Bounded by current subproblem $[L, R)$:
$$\text{cross\_start} = \max(L, M - k + 1)$$
$$\text{cross\_end} = \min(R - k, M - 1)$$

Only at most $k - 1$ windows can cross the midpoint. Each crossing window is checked against the precomputed source index.

---

### Q4: How do you verify matches and eliminate hash collisions?
**Answer:**
Whenever a suspect $k$-window queries the source hash index and finds candidate matching positions in the source text, the algorithm runs `verify_window_match()`. This function performs an exact word-by-word sequence check across all $k$ words. If any word differs, the match is discarded as a hash collision. This guarantees zero false positives.

---

### Q5: How do you merge overlapping matching windows into passages?
**Answer:**
Individual $k$-word matches often overlap (for example, windows $[1..3]$ and $[2..4]$ matching source $[0..2]$ and $[1..3]$). The `merge_intervals()` function sorts all unique matches and extends a passage whenever:
1. $s_{\text{start}} \le \text{prev\_}s_{\text{end}} + 1$
2. $(s_{\text{start}} - \text{prev\_}s_{\text{start}}) = (src_{\text{start}} - \text{prev\_}src_{\text{start}})$ (preserves relative alignment)

This produces maximal contiguous passages (e.g. $[1..6]$ with length 6 words).

---

### Q6: How is the similarity percentage calculated?
**Answer:**
$$\text{Similarity} = \left(\frac{\text{Unique Copied Suspect Words}}{\text{Total Suspect Words}}\right) \times 100$$
We compute the mathematical set union of all suspect word indices covered by any merged passage. This guarantees that overlapping passages do not double-count suspect words.

---

### Q7: Walk me through the UPES Reference Example:
**Answer:**
- **Source:** *"the quick brown fox jumps over the lazy dog near the river bank"* (13 words)
- **Suspect:** *"yesterday the quick brown fox jumps over a sleeping dog near the river bank today"* (15 words)
- **Window size $k$:** 3
- **Identified Passages:**
  1. *"the quick brown fox jumps over"* — Suspect positions $[1..6]$, Length 6 words
  2. *"dog near the river bank"* — Suspect positions $[9..13]$, Length 5 words
- **Total Copied Suspect Words:** $6 + 5 = 11$ words out of 15.
- **Similarity Percentage:** $\frac{11}{15} \times 100 = 73.33\%$.

---

### Q8: What are the theoretical and measured complexities?
**Answer:**
- **Divide and Conquer:**
  - Recurrence: $T(n) = 2T(n/2) + O(k)$
  - By Master Theorem: $\Theta(N)$ search time, with total time $O(M + N \log N)$.
  - On 2,000 words: took **0.035 seconds** (2,356 comparisons).
  - On 105,000 words: took **2.11 seconds**!
- **Brute Force:**
  - Time: $O(N \cdot M \cdot k)$.
  - On 2,000 words: took **4.04 seconds** (4,032,042 comparisons).
  - On 100,000 words: estimated $> 10$ hours (infeasible).
- **Speedup:** D&C is $> 110\times$ faster on moderate texts and $> 15,000\times$ faster on large documents.

---

### Q9: What edge cases did you test?
**Answer:**
We tested 15 mandatory edge cases in automated pytest suites:
1. Empty suspect document
2. Empty source document
3. Documents shorter than $k$
4. Identical documents (100% similarity)
5. Independent/disjoint documents (0% similarity)
6. Repeated words (extreme collision test)
7. Multiple copied passages
8. Overlapping matches
9. Match crossing the midpoint
10. Match at the beginning (index 0)
11. Match at the end
12. Invalid inputs (None, whitespace, symbols)
13. Unreadable/corrupted files
14. Scalability sanity (1,000 words)
15. Different $k$ values ($k \in \{1, 2, 3, 5, 8\}$)
All 35 tests pass with 100% success rate.
