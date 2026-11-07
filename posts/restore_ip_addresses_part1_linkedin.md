# Partitioning IPv4: Pruning the Search Envelope (Part 1 of 2) 🌐

**The Problem**:
Given a string of digits `s`, restore all valid IPv4 addresses formed by inserting dots.
Each of the 4 octets must be between 0 and 255 with no leading zeros (except `"0"` itself).
Example: `"25525511135"` yields `["255.255.11.135", "255.255.111.35"]`.

---

### 🧩 The Combinatorial Slicing Pitfalls

When tackling string partitioning, standard DFS often incurs subtle performance leaks:
1️⃣ **Unchecked Bounds**: If `s` has 20 digits, naive recursion still explores branches before failing at the tail.
2️⃣ **Heap Allocation Storm**: Passing `segments + [segment]` creates brand new lists on every branch.
3️⃣ **Redundant Branching on Zeros**: If an octet starts with `'0'`, testing lengths 2 and 3 (`"00"`, `"01"`) wastes CPU cycles when multi-digit numbers with leading zeros are strictly forbidden.

Can we turn backtracking into a deterministic, surgical search?

---

### 💡 3 Key Invariants for High-Performance Search

1️⃣ **The Feasibility Envelope**:
An IPv4 address has exactly 4 octets, each of length 1 to 3.
- **Global Guard**: The total string length must satisfy $4 \le \text{len}(s) \le 12$. If out of bounds, return `[]` in $O(1)$!
- **Remaining Envelope**: At any depth, with $k = 4 - \text{len}(path)$ octets remaining and $rem = n - start$ digits left:
$$k \le rem \le 3 \cdot k$$
Any branch violating this constraint is aborted immediately—no exploration needed!

2️⃣ **Leading Zero Short-Circuit**:
If `s[start] == '0'`, the ONLY valid octet starting at this index is `"0"`.
We restrict `max_len = 1` and never test lengths 2 or 3!

3️⃣ **In-Place Path Buffer**:
Using a mutable list with `path.append(sub)` and `path.pop()` bounds auxiliary memory to $O(1)$ depth.

---

### 📊 Complexity

- **Time:** $O(1)$ deterministic upper bound. The recursion tree has depth 4 with at most 3 branches per node (at most $3^4 = 81$ leaf checks).
- **Auxiliary Space:** $O(1)$ stack frames and path buffer.

---

### 🚀 What's Next?

DFS with envelope pruning runs in microseconds.
Notice something special about IPv4:
There are **exactly 3 internal dots**, each with at most 3 choices!
Total possible partition points: $3 \times 3 \times 3 = \mathbf{27}$!

In Part 2, we contrast backtracking with:
1. **The 27-Iteration Flat Loop**: Zero recursion, pure 3-nested loops.
2. **Layer-by-Layer Dynamic Programming**: Generalizing partition problems to arbitrary segments.

Do you prefer recursive DFS or flat nested loops for fixed-split problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #LeetCode #CodingInterview #SoftwareEngineering
