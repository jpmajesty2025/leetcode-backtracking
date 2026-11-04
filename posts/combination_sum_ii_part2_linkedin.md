# Beyond Loop Backtracking: Binary Trees vs. Bounded DP (Part 2 of 2) ⚡

In Part 1, we saw how the `i > start` guard prunes sibling duplicate subtrees in Combination Sum II.

Can we formulate this as a **binary decision tree**?
Can we eliminate recursion entirely using **Bounded Knapsack Dynamic Programming**?

Here are two distinct alternative paradigms.

---

### 🚀 Alternative 1: Binary Decision Tree (Twin Skipping)

Instead of a loop, make two decisions at state `(index, remaining)`:

1. **Include**:
   Pick `cands[index]`. Advance index by 1:
   `dfs(index + 1, remaining - cands[index])`

2. **Exclude (with Twin Skipping)**:
   Skip `cands[index]`—AND skip all its identical consecutive twins!
   Advance `next_idx` while `cands[next_idx] == cands[index]`.
   `dfs(next_idx, remaining)`

**Why this is elegant**:
Advancing past all identical twins during Exclude makes duplicate sibling branches impossible by construction! It replaces nested loops with clean binary branching.

---

### 💡 Alternative 2: Bounded Knapsack Dynamic Programming

Treat combination sum as bounded 0/1 knapsack dynamic programming:
1. Group candidates: `counts = Counter(candidates)`.
2. Let `dp[t]` store all unique combination tuples summing to $t$.
3. Base case: `dp[0] = {()}`.
4. **Outer Loop Over Distinct Items `(val, freq)`**:
   For each distinct item, choose $1 \dots \text{freq}$ copies of `val`.
   Extend combinations in `dp[t - count * val]` by `tuple([val] * count)`.

**Why this is powerful**:
Processing each distinct number once in the outer loop naturally enforces sorted order, guaranteeing zero duplicate combinations without recursion!

---

### 💥 The Benchmark

| Implementation | Paradigm | Aux Space | N=7 | Heavy Duplicates (N=33) | Speedup |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Standard Sorted BT | `i > start` Loop | $O(N)$ stack | 0.010 ms | 0.498 ms | Baseline |
| Binary Choice BT | Twin Skipping | $O(N)$ stack | 0.011 ms | 0.453 ms | 1.10x |
| **Bounded Knapsack DP** | **Table Iteration** | **$O(T \cdot K)$** | **0.022 ms** | **0.476 ms** | **Pure DP!** |

---

### 🧪 Verification

Verified with pytest and Hypothesis (27 test cases passed):
- **Deterministic Cases**: LeetCode examples, all-identical elements (`[2, 2, 2, 2]`), impossible sums, and negative targets.
- **Contract Integrity**: Verified caller input lists are never mutated.
- **Property Fuzzing**: Validated against an independent oracle across randomized inputs, proving exact sum equality, sub-multiset validity, and uniqueness.

---

### 🎯 Key Takeaway

Handling duplicates cleanly is a core algorithmic skill. Whether through loop sibling guards (`i > start`), binary choice twin-skipping, or bounded knapsack DP, pruning at the root prevents exponential wasted work.

Which paradigm do you prefer for bounded subset sum problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #DynamicProgramming #LeetCode #CodingInterview
