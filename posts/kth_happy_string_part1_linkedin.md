# The k-th Happy String: Pruning the Combinatorial Tree (Part 1 of 2) 🎭

**The Problem**:
A "happy string" uses letters `['a', 'b', 'c']` such that adjacent characters are never equal (`s[i] != s[i+1]`).
Given integers $n$ and $k$, return the $k$-th lexicographical happy string of length $n$ (1-indexed), or `""` if fewer than $k$ exist.

---

### 🧩 The Naive Trap: Generate, Store, and Slice

When finding the $k$-th item in a combinatorial space, a common reflex is:
1. Run DFS to generate all happy strings.
2. Store every string in a list (`result.append(current)`).
3. Return `result[k - 1]`.

Why is this suboptimal?
- **Heap Bloat**: Storing $k$ strings of length $n$ consumes $O(k \cdot n)$ heap space.
- **String Churn**: In Python, `current + char` creates a new string on every branch, straining the memory allocator.
- **Unchecked Search**: If $k$ exceeds total possible happy strings, naive DFS still explores the entire state space before returning `""`!

---

### 💡 3 Steps to Optimal Backtracking

1️⃣ **The O(1) Capacity Guard**:
How many happy strings of length $n$ exist?
- 1st character has **3** choices ('a', 'b', 'c').
- Each of the remaining $n - 1$ positions has **2** choices (any letter except the previous one).
$$\text{Total} = 3 \times 2^{n - 1}$$
If $k > 3 \times 2^{n - 1}$, abort immediately in $O(1)$! Zero search needed.

2️⃣ **In-Place Path Buffer**:
Replace string concatenation with a mutable list buffer (`path.append(char)` / `path.pop()`).
This bounds auxiliary memory strictly to $O(n)$ recursion depth.

3️⃣ **Short-Circuit Unwinding**:
Track completed strings with a leaf counter.
The instant `count == k`:
- Save `"".join(path)`.
- Return `True` up the call stack to immediately halt all further recursion!

---

### 📊 Complexity

- **Time:** $O(k \cdot n)$ worst-case. Halts immediately at leaf $k$.
- **Auxiliary Space:** $O(n)$ call stack and path buffer. Zero intermediate string heap allocations.

---

### 🚀 What's Next?

Backtracking solves this in $O(k \cdot n)$.
Notice the search tree structure: every node branches into exactly 2 children!
Can we compute the $k$-th string **directly in $O(n)$ time** with zero backtracking?

In Part 2, we explore:
1. **Direct Combinatorial Radix Math**: $O(n)$ time, $O(1)$ aux space (**395x faster**!).
2. **Iterative BFS Queue Expansion**: Eliminating recursion stacks.

How do you optimize your backtracking search: early capacity checks or short-circuit returns? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
