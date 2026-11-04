# Single-Use Combinatorics: The `i > start` Duplicate Filter (Part 1 of 2) 🎯

**The Problem**:
Given an array `candidates` (which may contain duplicates) and a target `target`, find all unique combinations that sum to `target`.
Each number may only be used **once** per combination.

---

### 🧩 The "Post-Hoc Deduplication" Trap

When numbers contain duplicates (e.g. `[10, 1, 2, 7, 6, 1, 5]`, target $8$), naive backtracking generates duplicates:
- Using the first `1`: `[1, 2, 5]`, `[1, 7]`
- Using the second `1`: `[1, 2, 5]`, `[1, 7]`

Calling `set(tuple(c) for c in result)` at the end wastes massive compute exploring redundant branches and allocating throwaway objects.

Can we prune duplicates **at the root of the branch**?

---

### 💡 The `i > start` Sibling Guard

Sort `candidates` upfront!
Then inside the backtracking loop:

```text
for i in range(start, len(cands)):
    if cands[i] > remaining:
        break
    if i > start and cands[i] == cands[i - 1]:
        continue
```

**Why `i > start` is pure genius**:
Consider duplicate twins `[1a, 1b]` at `start = 0`:

1. **Child Paths (Within the same depth path)**:
   When `i == start == 0`:
   We pick `1a`. It recurses with `start = 1`.
   At the next depth, `i == start == 1`:
   It picks `1b`!
   Because `i == start` (not `i > start`), the guard is **False**, so `1b` is accepted as a child of `1a`!
   This allows valid combinations like `[1, 1, 6]` to form!

2. **Sibling Paths (At the same recursion level)**:
   When `1a` finishes exploring its subtree and backtracks, the loop advances to `i = 1` (`1b`).
   Here, `i = 1` and `start = 0`.
   Now **`i > start` is True**, and `cands[1] == cands[0]`!
   The guard skips `1b`!
   Why? Because any combination formed starting with `1b` would be an **exact duplicate clone** of the combinations already generated starting with `1a`!

---

### ✂️ Instant Subtree Pruning with `break`

Because candidates are sorted:
If `cands[i] > remaining` $\implies$ **`break`**!
All subsequent candidates $j > i$ are even larger. A single `break` prunes the entire loop and all subtrees below it!

---

### 📊 Complexity

- **Time:** $O(2^N)$ worst-case upper bound. Duplicate pruning and early `break` restrict traversal strictly to valid branches.
- **Auxiliary Space:** $O(N)$ recursion call stack space.

---

### 🚀 What's Next?

In Part 2, we contrast loop backtracking with two alternate paradigms:
1. **Binary Choice Trees**: Strict Include / Exclude with twin skipping.
2. **Bounded Knapsack DP**: Table-driven combination building running in $0.47$ ms!

Did you know how `i > start` distinguishes parent-child duplicates from sibling duplicates? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
