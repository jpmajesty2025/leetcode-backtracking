# Grid Backtracking: The In-Place Sentinel Secret (Part 1 of 2) 🔍

**The Problem**:
Given an $m \times n$ grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.
The word can be constructed from sequentially adjacent cells (up, down, left, right).
Each cell may only be used **once** per word path.

---

### 🧩 The "Visited Set" Allocation Tax

The textbook way to avoid revisiting cells in grid DFS is to pass a `visited` set:
- Before recursing: `visited.add((r, c))`
- After recursing: `visited.remove((r, c))`

While conceptually clean, this introduces severe hidden costs in Python:
1️⃣ **Tuple Allocation**: Every candidate cell step allocates a temporary tuple `(r, c)`.
2️⃣ **Hash Table Overhead**: Inserting, hashing, checking collisions, and removing tuples across millions of branch evaluations consumes substantial CPU time.
3️⃣ **Auxiliary Memory**: A hash set consumes $O(M \cdot N)$ dynamic heap memory.

Can we achieve the exact same visited guard with **zero allocations**?

---

### 💡 The Sentinel In-Place Mutation Technique

Instead of an external hash set, treat the grid itself as its own visited map:

```text
temp = board[r][c]
board[r][c] = '#'      # Mark as visited with sentinel
found = (dfs(r+1, c) or dfs(r-1, c) or dfs(r, c+1) or dfs(r, c-1))
board[r][c] = temp     # Backtrack: restore original character
```

**Why this is way better!**:
1. **Zero Heap Allocations**: No tuples, no hash sets, no heap reallocations.
2. **Instant Rejection**: If an adjacent path loops back onto this cell, `board[r][c] == '#'`, which will never match any valid alphanumeric character in `word`!
3. **True $O(1)$ Auxiliary Space**: Only the recursion stack depth $O(L)$ is used.

---

### ⚡ Short-Circuit Branch Evaluation

Notice the chain of directional calls:
`dfs(r+1, c) or dfs(r-1, c) or dfs(r, c+1) or dfs(r, c-1)`

Using Python's logical `or`, evaluation short-circuits the microsecond any branch returns `True`. The remaining 3 directions are never explored, immediately collapsing the recursion stack back to the caller!

---

### 📊 Complexity

- **Time:** $O(M \cdot N \cdot 3^L)$ where $L$ is word length. From any cell, the initial step has 4 directions, but subsequent steps have at most 3 directions because we cannot immediately revisit the parent cell.
- **Auxiliary Space:** $O(L)$ recursion stack space (versus $O(M \cdot N)$ with visited sets).

---

### 🚀 What's Next?

In Part 2, we expose an adversarial test case that causes standard backtracking to **Time Out (TLE)**—and reveal how a **directional reversal trick** slashes runtime by **over 1,000x**!

Do you use in-place grid mutation or hash sets for 2D backtracking? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
