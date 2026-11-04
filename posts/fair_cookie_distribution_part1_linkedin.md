# Minimax Partitioning: The (k - 1)! Symmetry Break (Part 1 of 2) 🍪

**The Problem**:
You have an array of cookie bags `cookies` and $k$ children.
All cookies in the same bag must go to the same child.
The **unfairness** of a distribution is the maximum total cookies obtained by any single child.
Return the minimum possible unfairness.

---

### 🧩 The $k^N$ Combinatorial Explosion

With $N$ bags and $k$ children, every bag can be assigned to any of the $k$ children.
The naive state space size is:
$$k^N$$
For $N = 8, k = 8$:
$$8^8 = 16,777,216\text{ distributions!}$$

Exploring 16 million paths causes brute force search to hit **Time Limit Exceeded (TLE)**.

Can we prune this search space down to fewer than a few hundred nodes?

---

### 💡 Secret 1: Symmetry Breaking of Empty Children

At the root of the recursion, all $k$ children have $0$ cookies.
They are completely indistinguishable!
Giving bag 0 to child 0, child 1, or child 7 generates **exact isomorphic duplicate subtrees**!

**The Golden Symmetry Guard**:
```python
child_sums[i] += bag
dfs(idx + 1, max(current_max, child_sums[i]))
child_sums[i] -= bag

if child_sums[i] == 0:
    break
```

If `child_sums[i] == 0` after backtracking, that child was empty before receiving this bag.
Trying to assign this bag to any subsequent empty child would produce the exact same distribution with renamed children!
Breaking immediately eliminates $(k - 1)!$ redundant permutations!
For $k = 8$, this prunes **$7! = 5,040\times$ fewer permutations**!

---

### ✂️ Secret 2: Descending Sort & Branch-and-Bound

1. **Sort `cookies` Descending**:
   Distribute the largest bags first!
   Placing large numbers early forces child totals to rise quickly, which triggers upper-bound pruning near the root of the tree rather than at leaf nodes.

2. **Branch-and-Bound Cutoffs**:
   - `if current_max >= min_unfairness: return`
   - `if child_sums[i] + bag >= min_unfairness: continue`
   The moment any child's load exceeds the best known global answer, abort the branch!

---

### 📊 Complexity

- **Time:** $O(k^N)$ theoretical upper bound. With descending sort, symmetry breaking, and branch-and-bound cutoffs, actual explored states drop from 16 million to under $500$!
- **Auxiliary Space:** $O(N + k)$ recursion stack and bucket array.

---

### 🚀 What's Next?

In Part 2, we contrast Branch-and-Bound with two alternate paradigms:
1. **Binary Search on the Answer**: Converting optimization to decision search for a **10x speedup**!
2. **Bitmask Dynamic Programming**: Submask iteration in $O(k \cdot 3^N)$ time.

How do you tackle minimax partitioning problems: Branch-and-Bound or Binary Search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #DynamicProgramming #LeetCode #CodingInterview
