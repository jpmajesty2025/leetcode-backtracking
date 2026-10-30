# Graph Backtracking: The No-Visited DAG Theorem (Part 1 of 2) 🗺️

**The Problem**:
Given a Directed Acyclic Graph (DAG) of $N$ nodes labeled $0$ to $N - 1$, find all possible paths from source node $0$ to destination node $N - 1$ in any order.

---

### 🧩 The "Visited Set" Reflex

In almost every introductory graph algorithm—BFS, DFS, Dijkstra, Cycle Detection—we are taught:
*"Always maintain a `visited` set to prevent infinite cycles!"*

Naturally, when developers first approach this problem, their immediate instinct is:
- Mark `visited.add(node)`
- Recurse on neighbors
- Unmark `visited.remove(node)` upon return

**Is a visited set actually needed here?**
No! Look closely at the problem statement:
The graph is guaranteed to be a **Directed Acyclic Graph (DAG)**.

---

### 💡 Why DAGs Grant Immune Status to Backtracking

By definition, a DAG contains **zero directed cycles**:
If you follow directed edges from node $u$, it is mathematically impossible to ever reach node $u$ again along that same path.

Because no path can encounter an already-visited node along its current trajectory, an infinite recursion loop is impossible!
- You do **not** need a `visited` set to prevent cycles.
- You do **not** need cycle detection logic.

A single mutable `path = [0]` passed down the call tree with symmetrical `path.append(neighbor)` and `path.pop()` is completely sufficient and memory-safe!

---

### ⚠️ The Exponential Nature of DAG Paths

Even though the graph has at most $15$ nodes ($N \le 15$), how many paths can exist between node $0$ and node $N - 1$?

Consider a **dense complete DAG** where every node $i$ has a directed edge to every node $j > i$:
- Intermediate nodes are $\{1, 2, \dots, N - 2\}$ (a total of $N - 2$ nodes).
- Any subset of these intermediate nodes, traversed in strictly increasing order, forms a valid path from $0$ to $N - 1$!

The total number of paths in the worst case is:
$$\text{Total Paths} = 2^{N - 2}$$

For $N = 15$:
$2^{13} = 8,192\text{ distinct paths}$!
Because each path has an average length of $N / 2$, copying paths into the output takes $O(N \cdot 2^{N - 1})$ work. This exponential complexity is inherent to generating all paths!

---

### 📊 Complexity

- **Time:** $O(2^{N - 1} \cdot N)$ in worst-case dense DAGs. Every path must be written out to the result list.
- **Auxiliary Space:** $O(N)$ for the recursion call stack and active `path` buffer (excluding the $O(2^{N - 1} \cdot N)$ output list).

---

### 🚀 What's Next?

In Part 2, we contrast DFS backtracking with two alternative paradigms:
1. **BFS Queue Expansion**: Level-order path discovery by hop count.
2. **Top-Down Memoized DP**: Caching suffix paths across overlapping DAG subproblems!

Do you instinctively reach for a `visited` set whenever you see graph DFS? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Backtracking #GraphTheory #LeetCode #CodingInterview
