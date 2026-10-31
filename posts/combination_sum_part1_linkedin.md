# Unbounded Backtracking: The Sorting Pruning Power Law (Part 1 of 2) 🎯

**The Problem**:
Given an array of distinct integers `candidates` and an integer `target`, return all unique combinations where the numbers sum to `target`. Each number may be chosen an **unlimited** number of times.

---

### 🧩 The Two Traps in Unbounded Search

When candidate numbers can be picked repeatedly, two traps easily cripple performance:

1️⃣ **The Duplicate Permutation Trap**:
If you search from index $0$ on every branch, you generate `[2, 3, 2]`, `[3, 2, 2]`, and `[2, 2, 3]` as separate paths.
Filtering duplicates with `set(tuple(...))` after the fact wastes massive compute exploring redundant branches.
**The Fix**:
Pass the current candidate index `start = i` forward!
By allowing the next choice to come only from indices $\ge i$, elements are chosen in non-decreasing order of index, guaranteeing that each combination is discovered in a single canonical form.

2️⃣ **The Blind Exploration Trap**:
Consider an unsorted array where candidate $c > \text{remain}$.
In naive backtracking, the loop continues checking every remaining element in the list, recursing deeper and hitting `current_sum > target` base cases over and over again!

---

### ✂️ The Power of Sorting Upfront

Sort `candidates` in ascending order before recursing!

Because candidates are in strictly non-decreasing order:
$$cands[0] \le cands[1] \le \dots \le cands[N - 1]$$

The moment any candidate exceeds the remaining target:
$$\text{If } cands[i] > \text{remain} \implies \mathbf{break}$$

Not `continue`—**`break`**!
Because all subsequent candidates $j > i$ are even larger, they are guaranteed to exceed `remain`.
A single `break` statement instantly aborts the entire loop, pruning vast subtrees of doomed recursive branches!

---

### 💡 Decrementing Target vs. Sum Accumulation

Instead of passing `current_sum` and testing `current_sum == target`:
- Initialize with `remain = target`.
- Recurse with `remain - cands[i]`.
- Terminate when `remain == 0`.

This simplifies base case checks and keeps state tracking clean and cache-friendly.

---

### 📊 Complexity

- **Time:** $O(N^{T / M + 1})$ upper bound, where $N$ is candidate count, $T$ is target, and $M$ is the minimum candidate value (maximum recursion depth is $T / M$). Sorted branch pruning dramatically cuts the effective branching factor.
- **Auxiliary Space:** $O(T / M)$ recursion stack depth and path buffer.

---

### 🚀 What's Next?

In Part 2, we contrast backtracking with two alternate paradigms:
1. **Binary Choice Trees**: Strict include/exclude decisions without loops.
2. **Bottom-Up Dynamic Programming**: Coin-change table building running **2.5x faster**!

Do you prefer loop-based backtracking or binary include/exclude trees for unbounded knapsack problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #DynamicProgramming #LeetCode #CodingInterview
