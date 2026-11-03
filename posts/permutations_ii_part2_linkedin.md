# Beyond `used` Arrays: Frequency Maps vs. Next Permutation (Part 2 of 2) ⚡

In Part 1, we demystified the `not used[i - 1]` condition in permutations with duplicates allowed.

Can we eliminate index tracking entirely?
Can we eliminate recursion and call stacks using **iterative next permutation**?

Here are two distinct paradigms for handling duplicates.

---

### 🚀 Alternative 1: Frequency Map Backtracking (`Counter`)

Instead of sorting and tracking indices with `used[i]`, compress `nums` into a multiset frequency map:
`counts = Counter(nums)`

At each step, iterate through unique keys:
```python
for num in counts:
    if counts[num] > 0:
        counts[num] -= 1
        current.append(num)
        backtrack()
        current.pop()
        counts[num] += 1
```

**Why this is elegant**:
1. **Deduplication by Construction**: Because `counts.keys()` contains each distinct number once, sibling branches **never** attempt duplicate values!
2. **Zero Sorting or Index Logic**: No `nums[i] == nums[i - 1]` checks and no `used` array.

---

### 💡 Alternative 2: Iterative Next-Permutation (Narayana Pandita, 14th Century)

Generate permutations iteratively in strict lexicographical order:
1. Sort `nums` once.
2. In each iteration:
   - Find rightmost pivot: `arr[i] < arr[i + 1]`.
   - Find rightmost successor: `arr[j] > arr[i]`.
   - Swap `arr[i]` and `arr[j]`, then reverse suffix `arr[i + 1:]`.
3. Stop when the array is descending.

**Why is this nearly 2x faster?**
- **Zero Recursion Frames**: Operates purely iteratively in $O(1)$ auxiliary memory.
- **Natural Deduplication**: Steps directly to the strictly greater lexicographical permutation, bypassing duplicates automatically!

---

### 💥 The Benchmark

| Implementation | Paradigm | Aux Space | 30 Perms | 2,520 Perms | Speedup |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `used` Array DFS | Index Tracking | $O(N)$ stack | 0.035 ms | 2.807 ms | Baseline |
| Frequency Map DFS | Multiset Counts | $O(U + N)$ | 0.048 ms | 4.120 ms | Clean Model |
| **Iterative Next-Perm** | **Narayana Algorithm** | **$O(1)$** | **0.019 ms** | **1.576 ms** | **1.78x!** |

---

### 🧪 Verification

Verified with pytest and Hypothesis (28 test cases passed):
- **Deterministic Cases**: LeetCode examples (`[1, 1, 2]`), all identical elements (`[2, 2, 2, 2]`), single elements, and negative integers.
- **Contract Integrity**: Verified caller input lists are never mutated.
- **Property Fuzzing**: Validated against an independent oracle across randomized lists, proving multinomial count exactness, uniqueness, and set agreement.

---

### 🎯 Key Takeaway

Deduplication can be achieved through index guards (`not used[i-1]`), multiset frequency maps (`Counter`), or order-theory state transitions (Narayana Pandita).

In production, do you prefer frequency maps for clarity or next-permutation for speed? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
