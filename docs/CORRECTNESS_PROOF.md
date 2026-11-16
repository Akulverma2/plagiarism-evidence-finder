# Mathematical Correctness Proof
## Problem 17: Plagiarism Evidence Finder using Divide and Conquer
**University:** UPES, Dehradun  
**Course:** Design and Analysis of Algorithms (DAA)  
**Author:** Autonomous Engineering Agent  

---

## 1. Theorem Statement

Let $S = \langle s_0, s_1, \dots, s_{N-1} \rangle$ be a normalized suspect word sequence of length $N$, and let $T = \langle t_0, t_1, \dots, t_{M-1} \rangle$ be a normalized source word sequence of length $M$. Let $k \ge 1$ be the minimum match window size.

A window $W_i = \langle s_i, s_{i+1}, \dots, s_{i+k-1} \rangle$ starting at index $i \in [0, N-k]$ in $S$ is a **valid matching window** if and only if there exists at least one index $j \in [0, M-k]$ such that:
$$s_{i+r} = t_{j+r} \quad \forall r \in \{0, 1, \dots, k-1\}$$

**Theorem:** The `divide_and_conquer(S, 0, N, k, source_index, T)` algorithm terminates and returns every valid matching window $(i, i+k-1, j, j+k-1)$ without omission and without duplication.

---

## 2. Strong Mathematical Induction Proof

We prove correctness by strong mathematical induction on the length of the suspect subproblem range $L = \text{right} - \text{left}$.

### 2.1 Base Cases

#### Case 1: $L < k$
- When the subproblem length is strictly less than $k$, it is physically impossible for any $k$-word window to be contained within $[\text{left}, \text{right})$.
- The algorithm evaluates `if length < k: return []`.
- This correctly outputs zero matches.

#### Case 2: $L = k$
- When the subproblem length is exactly $k$, there is exactly one window starting at index $\text{left}$, spanning $[\text{left}, \text{left} + k - 1]$.
- The algorithm checks this single window directly via hash table lookup in `source_index` and verifies character-by-character equality against candidate source positions.
- If a match exists, it is recorded; otherwise, it is rejected.
- Since no subproblem division occurs, termination is immediate and the output is exact.

---

### 2.2 Inductive Hypothesis

Assume that for all subproblems with range length $L'$ such that $k \le L' < L$, the recursive function `divide_and_conquer` correctly finds and returns all valid matching $k$-word windows starting at indices within the range without omission or duplication.

---

### 2.3 Inductive Step ($L > k$)

Consider a subproblem defined on the range $[\text{left}, \text{right})$ with length $L = \text{right} - \text{left} > k$.
Since $L > k \ge 1$, we have $L \ge 2$.

The algorithm calculates the midpoint:
$$\text{mid} = \text{left} + \left\lfloor \frac{L}{2} \right\rfloor$$

Because $L \ge 2$:
$$\text{left} < \text{mid} < \text{right}$$
$$\text{left\_length} = \text{mid} - \text{left} < L$$
$$\text{right\_length} = \text{right} - \text{mid} < L$$

Both recursive subproblems have strictly smaller lengths, ensuring termination.

Now, consider any valid $k$-word window starting at index $i \in [\text{left}, \text{right} - k]$. The window occupies the index set:
$$\mathcal{W}(i) = \{i, i+1, \dots, i+k-1\}$$

Every starting index $i$ must satisfy exactly one of the following three mutually exclusive and collectively exhaustive conditions:

#### Case A: Entirely in the Left Half
- The window ends strictly before or at $\text{mid}$:
  $$i + k - 1 < \text{mid} \iff i \le \text{mid} - k$$
- The window is entirely contained within $[\text{left}, \text{mid})$.
- By the inductive hypothesis, the recursive call `divide_and_conquer(S, left, mid, k, ...)` correctly finds all matching windows in this range.

#### Case B: Crossing the Midpoint
- The window starts strictly before $\text{mid}$ AND ends at or after $\text{mid}$:
  $$i < \text{mid} \quad \text{and} \quad i + k - 1 \ge \text{mid}$$
  $$\iff \text{mid} - k + 1 \le i \le \text{mid} - 1$$
- Constrained by the subproblem boundary $[\text{left}, \text{right} - k]$, the valid range of starting indices for crossing windows is:
  $$i \in [\max(\text{left}, \text{mid} - k + 1), \, \min(\text{right} - k, \text{mid} - 1)]$$
- The procedure `find_crossing_matches()` iterates through every index in this exact interval, queries the precomputed source index, and verifies exact word sequences.
- Thus, every crossing match is identified.

#### Case C: Entirely in the Right Half
- The window starts at or after $\text{mid}$:
  $$i \ge \text{mid}$$
- The window is entirely contained within $[\text{mid}, \text{right})$.
- By the inductive hypothesis, the recursive call `divide_and_conquer(S, mid, right, k, ...)` correctly finds all matching windows in this range.

---

### 2.4 Partition Completeness and Disjointness

To prove that no windows are missed and no windows are double-counted, observe the union and intersection of the index ranges:
$$\mathcal{I}_{\text{left}} = [\text{left}, \, \text{mid} - k]$$
$$\mathcal{I}_{\text{cross}} = [\text{mid} - k + 1, \, \text{mid} - 1]$$
$$\mathcal{I}_{\text{right}} = [\text{mid}, \, \text{right} - k]$$

Notice:
1. $\mathcal{I}_{\text{left}} \cap \mathcal{I}_{\text{cross}} = \emptyset$ (since $\text{mid} - k < \text{mid} - k + 1$).
2. $\mathcal{I}_{\text{cross}} \cap \mathcal{I}_{\text{right}} = \emptyset$ (since $\text{mid} - 1 < \text{mid}$).
3. $\mathcal{I}_{\text{left}} \cap \mathcal{I}_{\text{right}} = \emptyset$ (since $\text{mid} - k < \text{mid}$).
4. $\mathcal{I}_{\text{left}} \cup \mathcal{I}_{\text{cross}} \cup \mathcal{I}_{\text{right}} = [\text{left}, \, \text{right} - k]$.

Because the three index sets form a true partition of $[\text{left}, \text{right} - k]$, every starting index is considered **exactly once**.

By strong mathematical induction, the algorithm correctly finds all matching $k$-word windows for any input size $N \ge 0$. $\blacksquare$

---

## 3. Correctness of Interval Merging (`merge_intervals`)

1. Let $\mathcal{M}$ be the set of identified matching $k$-word window pairs $(s_i, s_i+k-1, t_j, t_j+k-1)$.
2. We sort $\mathcal{M}$ by $(s_i, t_j)$.
3. Two matching windows $W_1 = [s_1, e_1, t_1, u_1]$ and $W_2 = [s_2, e_2, t_2, u_2]$ are contiguous extensions of the same copied passage if and only if:
   $$s_2 \le e_1 + 1 \quad \text{and} \quad (s_2 - s_1) = (t_2 - t_1)$$
4. The algorithm extends $e_1 = \max(e_1, e_2)$ and $u_1 = \max(u_1, u_2)$ when this condition holds, and begins a new passage otherwise.
5. This corresponds directly to finding the maximal connected components in the interval graph of contiguous alignments.
6. Hence, every merged passage represents a maximal contiguous plagiarized substring. $\blacksquare$

---

## 4. Correctness of Similarity Calculation (`calculate_similarity`)

1. Plagiarism is defined as the fraction of suspect words that belong to at least one copied passage of length $\ge k$.
2. To prevent counting overlapping passages multiple times, the algorithm computes:
   $$\mathcal{C} = \bigcup_{p \in \text{Passages}} \{s \in \mathbb{N} \mid p.\text{suspect\_start} \le s \le p.\text{suspect\_end}\}$$
3. The copied word count is $|\mathcal{C}|$.
4. The overall similarity percentage is:
   $$\text{Similarity} = \frac{|\mathcal{C}|}{N} \times 100$$
5. Because $|\mathcal{C}|$ is computed via set union, no suspect word is counted more than once, satisfying the assignment requirement. $\blacksquare$
