# Bounded Search: Double-Ended Capacity Pruning (Part 1 of 2) 🎯

**The Problem**:
Find all valid combinations of $k$ distinct numbers from $1 \dots 9$ that sum up to $n$.
Each number may be used at most once.

---

### 🧩 The "Naive Loop" Trap

A straightforward backtracking loop tries each digit from `start` to `9`:
```text
for i in range(start, 10):
    if i > rem_sum: break
    backtrack(i + 1, rem_sum - i, rem_k - 1)
```

At first glance, `if i > rem_sum: break` looks like smart pruning.
**But is checking only the single-number bound enough?**
Consider what happens when $k = 4$ and $n = 1$:
The naive approach still dispatches recursive calls before failing deeper in the tree!
Or consider $k = 3, n = 24$, where `current = [1]`:
Can any 2 remaining numbers chosen from $2 \dots 9$ ever sum to $23$?
The maximum possible sum is $8 + 9 = 17 < 23$.
Yet naive backtracking explores thousands of doomed combinations trying to make up that impossible deficit!

---

### ✂️ The Double-Ended Capacity Pruning Technique

Because digits are drawn from the strictly bounded set $\{1, 2, \dots, 9\}$, we can calculate the **exact feasibility envelope** in $O(1)$:

1️⃣ **Global Bounds (Instant $O(1)$ Rejection)**:
- **Minimum achievable sum** of $k$ distinct digits:
  $$\text{min\_sum} = \sum_{j=1}^k j = \frac{k(k + 1)}{2}$$
- **Maximum achievable sum** of $k$ distinct digits:
  $$\text{max\_sum} = \sum_{j=10-k}^9 j = \frac{k(19 - k)}{2}$$
If $n < \text{min\_sum}$ or $n > \text{max\_sum}$, return `[]` immediately without ever touching recursion!

2️⃣ **Frame-Level Dynamic Envelope**:
At any recursion state with remaining digits `rem_k` starting from candidate `start`:
- Minimum sum possible: $\text{rem\_k} \cdot (2 \cdot \text{start} + \text{rem\_k} - 1) / 2$
- Maximum sum possible: $\text{rem\_k} \cdot (19 - \text{rem\_k}) / 2$

If `rem_sum` falls outside this achievable window, **abort the entire subtree immediately**!

3️⃣ **Forward-Looking Candidate Bound**:
To select `rem_k` candidates from $i \dots 9$:
$$i \le 9 - \text{rem\_k} + 1$$
Combining both constraints:
$$\text{upper\_limit} = \min(9 - \text{rem\_k} + 1, \text{rem\_sum})$$

---

### 📊 Complexity

- **Time:** $O(\binom{9}{k} \cdot k)$. With choices restricted to 9 numbers, there are at most $\binom{9}{4} = 126$ combinations. Capacity pruning reduces explored nodes to only productive paths.
- **Auxiliary Space:** $O(k)$ recursion stack depth and path buffer.

---

### 🚀 What's Next?

In Part 2, we contrast backtracking with two non-recursive paradigms:
1. **Bitmask Subset Filtering**: Testing the 512 subsets of $\{1 \dots 9\}$ in $O(1)$ time.
2. **`itertools.combinations`**: C-accelerated combinatorics running in microseconds!

Have you used arithmetic feasibility envelopes to prune combinatorial searches? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
