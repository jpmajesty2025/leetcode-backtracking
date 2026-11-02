# Digit Construction: Pure Arithmetic vs. String Churn (Part 1 of 2) 🔢

**The Problem**:
Given two integers $n$ and $k$, return an array of all integers of length $n$ where the difference between every two consecutive digits is $k$.
Integers must not contain leading zeros (except $0$ itself when $n = 1$).

---

### 🧩 The "String Buffer" Habit

When asked to construct numbers digit-by-digit, developers often reach for string concatenation:
- `current_str + str(next_digit)`
- Base case: `int(current_str)`

While functional, this approach carries heavy performance penalties:
1️⃣ **Constant Type Conversions**: `int -> str` on every step, followed by `str -> int` at every leaf.
2️⃣ **Heap Allocation Storm**: Creating and discarding intermediate strings across thousands of recursion paths strains Python's memory allocator.
3️⃣ **Inefficient Iteration**: Scanning `range(10)` and checking `abs(next_d - last_d) == k` executes 10 iterations where at most 2 can ever be valid!

---

### 💡 The Pure Integer Arithmetic Solution

We can eliminate strings, casting, and digit loops entirely!

1. **Grow Numbers with Modular Math**:
   Instead of string concatenation, use positional arithmetic:
   $$\text{next\_number} = \text{current\_number} \times 10 + \text{next\_digit}$$
   Pure integer operations execute directly in CPU registers without heap allocations!

2. **$O(1)$ Candidate Calculation**:
   Given the last digit `last_d`, what digits can follow?
   There are at most **two** candidates:
   - `last_d + k` (valid if $< 10$)
   - `last_d - k` (valid if $\ge 0$)
   No 10-digit loop needed—just two instantaneous arithmetic bounds checks!

---

### ⚠️ The $K = 0$ Duplicate Trap

What happens when $k = 0$?
`last_d + 0 == last_d - 0`!
If both branches execute when $k = 0$, every single number will be generated and appended **twice**!

**The Guard**:
Only explore the second branch if $k \ne 0$:
```text
next_d1 = last_d + k
if next_d1 < 10:
    dfs(..., num * 10 + next_d1)

if k != 0:
    next_d2 = last_d - k
    if next_d2 >= 0:
        dfs(..., num * 10 + next_d2)
```
This check prevents duplicate numbers without requiring expensive `set()` deduplication!

---

### 📊 Complexity

- **Time:** $O(2^{N - 1})$. Each digit branches into at most 2 valid next digits, generating at most $9 \cdot 2^{N - 1}$ numbers. Pure integer math builds each number in $O(1)$ time.
- **Auxiliary Space:** $O(N)$ recursion call stack space.

---

### 🚀 What's Next?

In Part 2, we eliminate recursion entirely and examine two non-recursive paradigms:
1. **Iterative BFS Layer Expansion**: Growing digits layer-by-layer running **6x faster**!
2. **Digit Dynamic Programming**: Subproblem bucketing by ending digit.

Do you default to strings or integer math when building numbers? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
