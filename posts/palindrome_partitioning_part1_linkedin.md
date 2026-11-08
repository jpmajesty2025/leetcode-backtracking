# Palindrome Partitioning: Pruning Slicing Overhead (Part 1 of 2) 🔁

**The Problem**:
Given a string `s`, partition it such that every substring in the partition is a palindrome.
Return all possible palindrome partitionings.
Example: `s = "aab"` yields `[["a", "a", "b"], ["aa", "b"]]`.

---

### 🧩 The Hidden Bottleneck in Standard DFS

Most implementations follow an intuitive backtracking pattern:
```python
def is_palindrome(sub: str) -> bool:
    return sub == sub[::-1]
```
While simple, this naive check carries substantial hidden costs:
1️⃣ **Slicing Churn**: `s[start:end]` allocates a new string on the heap.
2️⃣ **Reversal Overhead**: `sub[::-1]` allocates a second reversed string and compares characters in $O(L)$ time.
3️⃣ **Duplicate Re-Verification**: Across different partition branches, identical substrings (e.g., `s[2:6]`) are repeatedly sliced and re-checked over and over again!

Can we eliminate repeated string reversal and make palindrome checks instantaneous?

---

### 💡 The O(1) Solution: Precomputed 2D Palindrome Table

Instead of re-checking palindromes on the fly during search, **precompute all substring palindromes once** in $O(N^2)$ time!

**The Invariant**:
A substring `s[i:j]` is a palindrome if and only if:
1. Outer characters match: `s[i] == s[j]`
2. The inner substring is already a palindrome: `j - i <= 2 or is_pal[i + 1][j - 1]`

**The DP Precomputation**:
```python
is_pal = [[False] * n for _ in range(n)]
for i in range(n - 1, -1, -1):
    for j in range(i, n):
        if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
            is_pal[i][j] = True
```

**The Payoff During Backtracking**:
- Checking if `s[start:end]` is a palindrome becomes an **instant $O(1)$ table lookup** (`is_pal[start][end]`).
- Zero substring slicing on invalid branches.
- Zero string reversing.
- Slicing occurs **only** when a valid palindrome branch is confirmed!

---

### 📊 Complexity

- **Time:** $O(N^2 + 2^N \cdot N)$. Building the table takes $O(N^2)$. Generating all $2^{N - 1}$ partitions takes $O(2^N \cdot N)$, but with $O(1)$ checks instead of $O(N)$ checks per branch.
- **Auxiliary Space:** $O(N^2)$ for the 2D boolean table + $O(N)$ recursion depth.

---

### 🚀 What's Next?

Precomputing the palindrome table eliminates slicing churn.
Can we eliminate the recursion call stack entirely?
What happens if we formulate this as **Bottom-Up Iterative Dynamic Programming**?

In Part 2, we explore:
1. **Prefix Expansion DP**: Building partitions iteratively layer-by-layer.
2. **Performance Benchmarks**: How iterative DP runs **2.3x faster** on dense palindrome inputs!

Do you precompute tables or check on-the-fly when backtracking palindromes? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
