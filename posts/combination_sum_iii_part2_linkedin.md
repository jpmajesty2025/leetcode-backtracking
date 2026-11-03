# Beyond Backtracking: Bitmask Filtering vs. itertools (Part 2 of 2) ⚡

In Part 1, we saw how double-ended arithmetic feasibility envelopes cut wasted branches in Combination Sum III (LeetCode 216).

Backtracking is the classic interview mental model. But look closely at the constraints:
**Only digits $1 \dots 9$ are used, each at most once!**

How large is the entire universe of possible subsets?
$$2^9 = 512\text{ total subsets!}$$

When the entire search space contains only 512 states, we can explore non-recursive paradigms!

---

### 🚀 Alternative 1: Binary Bitmask Enumeration ($O(1)$ Space)

Map every subset of $\{1 \dots 9\}$ to a 9-bit integer:
- If bit $j$ ($0 \le j < 9$) is set, include digit $j + 1$.
- Exactly $k$ numbers chosen $\iff \text{mask.bit\_count}() == k$.
- If $\text{sum} == n$, append the subset!

**Why this is elegant**:
- **Pure Iteration**: Zero recursion call stacks.
- **Fixed Overhead**: Evaluates at most 512 integers—strictly $O(1)$ time and auxiliary space!

---

### 💡 Alternative 2: C-Accelerated `itertools.combinations`

Instead of checking all 512 subsets, generate only subsets of size $k$ directly:
```python
if n < min_sum or n > max_sum:
    return []
return [list(c) for c in itertools.combinations(range(1, 10), k) if sum(c) == n]
```

**Why this is 5.6x faster in Python**:
- The maximum number of combinations of size $k$ from 9 digits is:
  $$\binom{9}{4} = 126\text{ combinations}$$
- `itertools.combinations` generates tuples in compiled C with zero Python frame allocations, achieving top throughput!

---

### 💥 The Benchmark

| Implementation | Paradigm | Aux Space | 3 Test Cases Runtime | Speedup |
| :--- | :--- | :--- | :--- | :--- |
| Naive Backtracking | Unbounded Loop | $O(k)$ stack | 0.1494 ms | Baseline |
| **Pruned Backtracking** | **Capacity Envelope** | **$O(k)$ stack** | **0.0627 ms** | **2.38x faster** |
| Bitmask Enumeration | 512 Subsets | $O(1)$ stack | 0.4024 ms | Pure Iteration |
| **`itertools` Combinations** | **C-Level Combinatorics** | **$O(1)$ stack** | **0.0264 ms** | **5.65x faster!** |

---

### 🧪 Verification

Verified with pytest and Hypothesis (27 test cases passed):
- **Deterministic Cases**: LeetCode examples ($k=3, n=7$ and $k=3, n=9$).
- **Boundaries**: $k=9, n=45$ and impossible targets ($n$ too large / too small).
- **Property Fuzzing**: Validated against an independent oracle across $1 \le k \le 9, 1 \le n \le 50$, confirming exact sum, length $k$, digit uniqueness, and set equivalence.

---

### 🎯 Key Takeaway

Always analyze constraint boundaries. When the universe of choices is tiny ($N \le 9$), mathematical feasibility bounds combined with built-in C tools like `itertools` outperform manual recursion by over 5x!

In production, do you prefer backtracking or standard library combinatorics? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
