# Permutations with Duplicates: The `not used[i - 1]` Mystery (Part 1 of 2) 🧩

**The Problem**:
Given a collection of numbers `nums` that might contain duplicates, return all unique permutations in any order.
Example: `[1, 1, 2] -> [[1, 1, 2], [1, 2, 1], [2, 1, 1]]` (3 unique permutations, not 6).

---

### 🧩 The Most Confusing Line in Backtracking

In standard permutation backtracking with duplicate pruning, we sort the array and encounter this guard:

```text
if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
    continue
```

Why `not used[i - 1]`?
Why does checking `not used[i - 1]` prevent duplicate permutations, while checking `used[i - 1]` seems counter-intuitive?

---

### 💡 Sibling Branches vs. Child Branches

Consider the sorted array `nums = [1a, 1b, 2]`.

When choosing the element for the **first position** of our permutation:
1. We pick `1a`. It marks `used[0] = True`, recurses, and explores all permutations starting with `1a` (e.g. `[1a, 1b, 2]`, `[1a, 2, 1b]`).
2. When recursion returns, it unmarks `used[0] = False`.
3. The loop moves to index 1: candidate `1b`.
   Notice: `nums[1] == nums[0]`, and right now **`used[0]` is `False`**!
   If we choose `1b` as the first element, we would explore permutations starting with `1b`—which are **exact duplicate clones** of the ones we just produced with `1a`!

$\implies$ **`not used[i - 1]` means `nums[i - 1]` was already chosen as a sibling branch at this same level and has finished!** Skipping it prunes the duplicate branch immediately!

---

### 🔬 What if you wrote `and used[i - 1]` instead?

Both `not used[i - 1]` and `used[i - 1]` produce unique permutations!
**So why is `not used[i - 1]` the universal standard?**

- `used[i - 1]`: Enforces right-to-left duplicate selection.
- `not used[i - 1]`: Enforces left-to-right duplicate selection.

**The Massive Difference**:
With `not used[i - 1]`, pruning happens **at the shallowest possible level** (sibling branches).
On `[1, 1, 1, 2, 2]`:
- `not used[i - 1]` executes **34 total recursive calls**.
- `used[i - 1]` executes **99 total recursive calls** (nearly **3x more work**)!
`not used[i - 1]` slashes the recursion tree by **65%**!

---

### 📊 Complexity: Multinomial Formula

Total unique permutations follow the **multinomial coefficient**:
$$P = \frac{N!}{n_1! \cdot n_2! \dots n_k!}$$
- **Time:** $O(P \cdot N)$.
- **Auxiliary Space:** $O(N)$ for stack and `used` array.

---

### 🚀 What's Next?

In Part 2, we explore two alternate paradigms:
1. **Frequency Map Backtracking**: Elegant deduplication without sorting or `used` arrays.
2. **Narayana's Next Permutation**: Iterative generation running **nearly 2x faster** in $O(1)$ space!

Did you know why `not used[i-1]` is 3x faster than `used[i-1]`? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
