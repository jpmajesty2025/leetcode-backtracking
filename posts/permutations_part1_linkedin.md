# Backtracking Traps: The Hidden O(N² · N!) Allocation Tax (Part 1 of 2) 🔄

**The Problem**:
Given an array `nums` of distinct integers, return all possible permutations.
For an input of length $N$, there are exactly $N!$ distinct permutations.

---

### 🧩 The "Simple" Backtracking Pitfall

A common first-draft solution in Python often looks like this:
- Recurse with `backtrack(current)`
- Check candidate availability with `if num not in current`
- Recurse deeper with `backtrack(current + [num])`

It passes basic tests on small inputs. But under the hood, it conceals two major performance traps that sabotage efficiency:

1️⃣ **$O(N)$ Linear Scan per Candidate**:
`if num not in current` performs an $O(k)$ membership scan on a Python list at depth $k$. Across the $O(N!)$ decision tree, this adds unnecessary search overhead at every node.

2️⃣ **$O(N)$ List Concatenation & Heap Churn**:
Writing `backtrack(current + [num])` allocates a **brand new list** on *every branch* of the search tree!
The decision tree contains $\sum_{k=0}^N \frac{N!}{(N-k)!} \approx e \cdot N!$ nodes.
Allocating intermediate lists at every branch creates thousands of ephemeral heap objects, inflating time complexity from $O(N \cdot N!)$ to **$O(N^2 \cdot N!)$** and overloading garbage collection.

---

### 🔧 The Fix: Optimal State-Space Backtracking

To achieve optimal $O(N \cdot N!)$ complexity, eliminate linear scans and intermediate list copies:

1. **$O(1)$ Availability Tracking**:
   Use a boolean array `used = [False] * n` (or bitmask). Checking if an element has been picked is an immediate $O(1)$ lookup.
2. **In-Place Mutation with Symmetrical Push/Pop**:
   Instead of `current + [num]`, mutate a single reusable list:
   - Mark `used[i] = True`
   - `current.append(nums[i])`
   - `backtrack()`
   - `current.pop()`
   - Unmark `used[i] = False`
3. **Copy Only at the Leaves**:
   List copying happens exactly $N!$ times—only when adding a complete permutation to `result`.

---

### 📊 Complexity

- **Time:** $O(N \cdot N!)$. Constructing $N!$ leaves takes $O(N)$ copy work each. Every internal node transition runs in $O(1)$ time.
- **Auxiliary Space:** $O(N)$ call stack depth + $O(N)$ boolean array (excluding the $O(N \cdot N!)$ output list).

---

### 🚀 What's Next?

In Part 2, we eliminate the boolean `used` array entirely with **In-Place Swapping**, and examine a 14th-century algorithm by **Narayana Pandita** that generates permutations iteratively with **zero recursion stack** and a **4x speedup**!

Have you ever benchmarked `current + [item]` vs explicit push/pop backtracking in Python? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #SoftwareEngineering #CodingInterview
