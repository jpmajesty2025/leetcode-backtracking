# Beyond Backtracking: 3-Loop Partitions vs. Layer DP (Part 2 of 2) ⚡

In Part 1, we used envelope pruning to bound recursive DFS to microsecond speeds.
Backtracking works smoothly. But is recursion even necessary?

When a problem asks for a fixed number of splits, recursion can be replaced by direct iterative partition search!

---

### 🚀 Alternative 1: The 27-Iteration Flat Loop

An IPv4 address places **exactly 3 internal dots**, splitting `s` into:
`s[0:i]`, `s[i:j]`, `s[j:k]`, `s[k:n]`.

Because each segment length is in $\{1, 2, 3\}$, the partition ranges are tiny:
- $1 \le i \le 3$
- $1 \le j - i \le 3$
- $1 \le k - j \le 3$
- $1 \le n - k \le 3$

There are at most $3 \times 3 \times 3 = \mathbf{27}$ candidate triplets in the ENTIRE search space!
Three nested `for` loops evaluate all combinations directly without call stack frames or backtracking state mutations.

---

### 💡 Alternative 2: Layer-by-Layer Dynamic Programming

What if an address needed $K$ segments instead of 4?
Nested loops don't scale when $K$ is dynamic, but **bottom-up DP** does!

1. **State**: Let `dp[seg][end]` store valid prefixes for `s[:end]` using `seg` octets.
2. **Transition**: For stage $seg \in [2, 4]$, inspect trailing lengths $L \in \{1, 2, 3\}$.
   If `s[end - L : end]` is valid, extend all solutions from `dp[seg - 1][end - L]`.
3. **Extract**: Final answer lives in `dp[4][n]`.

This generalizes partition search cleanly to arbitrary segment counts!

---

### 💥 The Benchmark (Python 3.12, 10,000 runs)

| Input String | Paradigm | Aux Space | Backtracking | 3-Loop Iterative | Layer DP |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `"25525511135"` | DFS Envelope | $O(1)$ | 9.81 µs | 10.85 µs | 35.06 µs |
| `"101023"` | 3-Partition | $O(1)$ | 12.18 µs | **8.60 µs** | 20.54 µs |
| `"0000"` | Fixed Space | $O(1)$ | 2.97 µs | **2.05 µs** | 7.84 µs |
| `"1111"` | Fixed Space | $O(1)$ | 4.39 µs | **2.06 µs** | 10.86 µs |

---

### 🧪 Verification

Verified with pytest & Hypothesis (33 tests passed):
- **Deterministic Cases**: LeetCode examples, minimum valid (`"1111"`), maximum valid (`"255255255255"`), and leading zeros (`"010010"`).
- **Out-of-Bounds Guards**: Strings with $<4$ or $>12$ digits, non-digit characters (`"192.168@1.1"`), and octets $>255$.
- **Property Fuzzing**: Validated against an independent regex oracle (`re.compile(r"^(0|[1-9][0-9]{0,2})$")`).

---

### 🎯 Key Takeaway

When the number of partition splits is fixed and small, **replace recursion with flat nested loops**. When the number of segments is dynamic, use **layer-by-layer dynamic programming**.

Which paradigm is your default for fixed-split problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
