# Subsequences Without Sorting: Sibling Deduplication (Part 1 of 2) ⛓️

**The Problem**:
Given an integer array `nums`, return all distinct non-decreasing subsequences with at least two elements.
Example: `nums = [4, 6, 7, 7]` produces 8 unique subsequences, including `[4, 7]`, `[4, 7, 7]`, and `[7, 7]`.

---

### 🧩 The Sorting Trap

In classic duplicate-pruning (like Subsets II or Combination Sum II), the standard playbook is:
1. Sort `nums.sort()`.
2. Skip duplicates: `if i > start and nums[i] == nums[i - 1]: continue`.

**Why does this break here?**
Sorting rearranges the elements!
A **subsequence** requires preserving original relative order.
If `nums = [4, 4, 3, 2, 1]`, sorting yields `[1, 2, 3, 4, 4]`, completely corrupting the valid subsequences!
We must deduplicate in an **unsorted array**.

---

### ⚠️ The Global Set Workaround

When sorting is off the table, developers often fall back on a blunt instrument:
- Traverse all branches.
- Shove every path into a global set: `result.add(tuple(path))`.
- Post-process: `return [list(seq) for seq in result]`.

Why is this suboptimal?
1️⃣ **Allocation Storm**: Every path of length $\ge 2$ allocates a tuple on the heap.
2️⃣ **Hashing Overhead**: Python hashes every tuple element.
3️⃣ **Duplicate Exploration**: The recursion tree still explores identical subtrees.

---

### 💡 The Solution: Sibling Deduplication

We don't need global deduplication if we prune redundant branches at their origin!

**The Invariant**:
At any recursion depth, a fixed `path` is extended by elements in `nums[start:]`.
If the same value appears multiple times in `nums[start:]`, picking it a second time at this depth will only generate a duplicate subset of subsequences!

**The Sibling Guard**:
Create a `used` set **locally within each recursive frame**:
- Check non-decreasing condition: `not path or nums[i] >= path[-1]`
- Check sibling uniqueness: `nums[i] not in used`
- Record: `used.add(nums[i])`

**The Payoff**:
Because no sibling branch repeats the same value, **every generated leaf is guaranteed unique**!
We directly append `path[:]` to a plain Python list: `result.append(path[:])`—zero tuple conversions, zero hashing!

---

### 📊 Complexity

- **Time:** $O(2^N \cdot N)$ worst case ($N \le 15$). Non-decreasing pruning and sibling skips keep actual explored states tiny.
- **Auxiliary Space:** $O(N)$ call stack and path buffer. Zero tuple allocation overhead.

---

### 🚀 What's Next?

Backtracking with sibling guards is clean and memory-efficient.
Can we eliminate recursion entirely?
What about **Iterative Prefix Extension**? Or **Bitmask Enumeration** ($2^{15} \le 32,768$)?

In Part 2, we benchmark these non-recursive paradigms!

How do you handle deduplication when sorting is forbidden? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
