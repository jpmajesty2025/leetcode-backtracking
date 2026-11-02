# Beyond Backtracking: Bottom-Up Catalan Convolution DP (Part 2 of 2) ⚡

In Part 1, we saw how two balance invariants guarantee zero dead branches in parenthesis backtracking.

Can we compute valid parentheses bottom-up using **Catalan Decomposition Dynamic Programming**?

---

### 💡 The Catalan Decomposition Principle

Every non-empty well-formed sequence of size $k$ begins with `'('`.
Where is its **matching closing bracket** `')'`?

The matching `')'` splits the sequence into two independent well-formed sub-sequences:
$$\text{Sequence} = \mathbf{(} + A + \mathbf{)} + B$$
where:
- $A$ is a well-formed sequence of $c$ pairs ($0 \le c < k$)
- $B$ is a well-formed sequence of $k - 1 - c$ pairs

Since the matching `')'` for the first `'('` is located at index $2c + 1$, every pair of valid sequences $(A, B)$ generates a **unique** sequence of size $k$!

This directly mirrors the **Catalan recurrence relation**:
$$C_k = \sum_{c=0}^{k-1} C_c \cdot C_{k - 1 - c}$$

---

### 🚀 Bottom-Up Dynamic Programming

1. Initialize `dp = [[] for _ in range(n + 1)]`, with base case `dp[0] = [""]`.
2. For $k$ from $1$ to $n$:
   ```text
   for c in range(k):
       for left in dp[c]:
           for right in dp[k - 1 - c]:
               dp[k].append(f"({left}){right}")
   ```
3. Return `dp[n]`.

**Why is this up to 5x faster?**
- **Zero Recursion Frames**: Purely iterative loops with no stack limits.
- **Subproblem Reuse**: Combines precomputed substrings directly.
- **Guaranteed Unique**: The unique closing bracket position ensures zero duplicate strings are ever generated.

---

### 💥 The Benchmark

| Implementation | Paradigm | Aux Space | $N=8$ | $N=9$ | Speedup ($N=9$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Standard DFS | State-Space DFS | $O(n)$ stack | 1.058 ms | 3.970 ms | Baseline |
| BFS Queue | Level-Order BFS | $O(C_n)$ queue | 1.121 ms | 4.476 ms | Prefix order |
| **Catalan DP** | **Convolution DP** | **$O(C_n \cdot n)$** | **0.282 ms** | **0.768 ms** | **5.17x faster!** |

---

### 🧪 Verification

Verified with pytest and Hypothesis (24 test cases passed):
- **Deterministic Cases**: LeetCode examples, $n = 1, 2, 3, 4$, and boundary $n = 8$.
- **Catalan Exactness**: Verified exact sequence count $C_n = \frac{1}{n+1}\binom{2n}{n}$.
- **Structural Integrity**: Verified every string has length $2n$ and is balanced.
- **Property Fuzzing**: Validated against an independent oracle across $1 \le n \le 6$.

---

### 🎯 Key Takeaway

While backtracking explores the decision tree top-down, Catalan convolution constructs sequences bottom-up by combining subproblems, delivering top throughput with zero recursion stack overhead.

Have you implemented Catalan decomposition for parenthesis problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #DynamicProgramming #LeetCode #CodingInterview
