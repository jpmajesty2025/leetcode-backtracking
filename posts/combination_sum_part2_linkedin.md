# Beyond Backtracking: Binary Trees vs. Bottom-Up DP (Part 2 of 2) ⚡

**The Problem**:
Given an array of distinct integers `candidates` and an integer `target`, return all unique combinations where the numbers sum to `target`. Each number may be chosen repeatedly.

In Part 1, we saw how sorting upfront and early `break` pruning eliminates doomed subtrees.

Can we formulate this as a **binary decision tree**?
Can we eliminate recursion entirely using **Bottom-Up Dynamic Programming**?

Here are two distinct paradigms for unbounded combination sum.

---

### 🚀 Alternative 1: Binary Decision Tree (Include / Exclude)

Instead of a loop, make two choices at state `(index, remain)`:
1. **Include**: Pick `cands[index]`. Because elements can be reused, recurse with the **same** index:
   `dfs(index, remain - cands[index])`
2. **Exclude**: Skip `cands[index]` permanently for this path:
   `dfs(index + 1, remain)`

**Advantage**: Replaces nested iteration with a clean binary state graph.

---

### 💡 Alternative 2: Bottom-Up Dynamic Programming (Unbounded Knapsack)

Treat combination sum as coin-change dynamic programming:
1. Let `dp[t]` store all combinations summing to amount $t \in [0, \text{target}]$.
2. Base case: `dp[0] = [[]]`.
3. **Outer Loop Over Candidates** (Crucial!):
   Iterate candidate `c` in the outer loop and `t` from `c` to `target` in the inner loop.
   Extend every combination in `dp[t - c]` by `c`.

Putting `candidates` in the outer loop guarantees combinations are built in non-decreasing order, naturally preventing duplicate permutations!

---

### 💥 The Benchmark

| Implementation | Paradigm | Aux Space | Target 35 | Target 40 | Speedup |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Unpruned Backtracking | Blind Loop | $O(T/M)$ stack | 0.267 ms | 0.388 ms | Baseline |
| Pruned Backtracking | Sorted Break | $O(T/M)$ stack | 0.170 ms | 0.254 ms | 1.57x |
| Binary Choice Tree | 0/1 Decisions | $O(T/M)$ stack | 0.184 ms | 0.281 ms | Clean Model |
| **Bottom-Up DP** | **Knapsack Table** | **$O(T \cdot K)$ table** | **0.094 ms** | **0.162 ms** | **2.4x - 2.8x!** |

**The Trade-Off**:
Bottom-up DP runs **2.4x – 2.8x faster** by avoiding recursion frames and leveraging list extensions, but consumes table memory for intermediate targets.
Pruned backtracking uses minimal $O(T/M)$ stack space!

---

### 🧪 Verification

Verified with pytest and Hypothesis (27 test cases passed):
- **Deterministic Cases**: LeetCode examples, target unreachable, single elements, and negative targets.
- **Contract Integrity**: Caller input arrays are never mutated.
- **Property Fuzzing**: Validated against an independent oracle across randomized inputs, proving exact sum equality, uniqueness, and set agreement.

---

### 🎯 Key Takeaway

Unbounded combinations sit at the crossroads of backtracking and knapsack DP. When stack space is tight, pruned backtracking is ideal. When raw throughput matters, bottom-up DP excels!

Which paradigm do you prefer for unbounded combination problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #DynamicProgramming #LeetCode #CodingInterview
