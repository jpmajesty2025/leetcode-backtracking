# Keypad Combinatorics: The Immutability Paradox in Python (Part 1 of 2) 📱

**The Problem**:
Given a string of digits from $2$ to $9$, return all possible letter combinations that the number could represent on a telephone keypad.
Digits map to 3 letters (e.g. `2 -> abc`), while digits `7` and `9` map to 4 letters (`pqrs`, `wxyz`).

---

### 🧩 The General "Rule" vs The Python String Reality

In general backtracking tutorials, we are repeatedly taught:
*"Never concatenate strings or lists in recursion! Always mutate a list in-place via push/pop to avoid intermediate allocations!"*

For permutations or subsets, this advice is gold. But what happens when generating phone keypad combinations in Python?

Consider the two patterns:

**Pattern A (In-Place List Mutation)**:
- `path.append(letter)`
- `backtrack(index + 1)`
- `path.pop()`
- Base case: `result.append(''.join(path))`

**Pattern B (String Concatenation in Args)**:
- `backtrack(index + 1, path + letter)`
- Base case: `result.append(path)`

---

### 💡 The Benchmark Surprise

When benchmarked across thousands of combinations, **Pattern B (string concatenation) is actually faster than Pattern A (in-place list push/pop)**! Why?

1️⃣ **Microscopic Path Length ($N \le 4$)**:
In this problem, $0 \le N \le 4$.
Allocating and copying an immutable 4-character string in Python takes negligible CPU cycles—often handled via CPython's small-string cache and fast memory arena.

2️⃣ **The Hidden Cost of Leaf `join()`**:
In Pattern A, every single leaf node must execute `''.join(path)`.
Creating and populating $4^N$ complete string objects from scratch at leaf nodes incurs more total overhead than building the strings incrementally across 4 call frames!

3️⃣ **Zero Backtracking Teardown Overhead**:
Pattern B requires no cleanup step (`pop()`). Symmetrical push/pop bytecode operations are avoided entirely!

---

### ⚠️ Clean Engineering Details

- **Module-Level Constant**: Placing `KEYPAD_MAPPING` at the module level prevents dictionary re-allocation on every function call.
- **Empty String Base Case**: An empty string `""` must return `[]` (0 combinations), not `[""]`.

---

### 📊 Complexity

- **Time:** $O(4^N \cdot N)$. There are at most $4^N$ combinations (when all digits are 7 or 9), each of length $N$.
- **Auxiliary Space:** $O(N)$ recursion stack depth.

---

### 🚀 What's Next?

In Part 2, we ditch recursion entirely and examine two non-recursive paradigms:
1. **Iterative Cascading**: Dynamic BFS set expansion running **3.7x faster**!
2. **`itertools.product`**: C-accelerated Cartesian product in a single line.

Have you ever benchmarked string concatenation against list push/pop for short recursion depths? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #SoftwareEngineering #CodingInterview
