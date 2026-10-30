"""
LeetCode 797: All Paths From Source to Target
https://leetcode.com/problems/all-paths-from-source-to-target/

Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all
possible paths from node 0 to node n - 1 and return them in any order.

The graph is given as follows: graph[i] is a list of all nodes you can visit from
node i (i.e., there is a directed edge from node i to node graph[i][j]).

Constraints:
- n == graph.length
- 2 <= n <= 15
- 0 <= graph[i][j] < n
- graph[i][j] != i (no self-loops)
- All the elements of graph[i] are unique.
- The input graph is guaranteed to be a DAG.

Complexity:
- Time: O(2^(N - 1) * N) in the worst case (a dense DAG where every node i has directed
  edges to all j > i, producing 2^(N - 2) paths of average length N / 2). Each path
  takes O(N) to copy into the output list.
- Space: O(N) auxiliary space for the recursion call stack and active path buffer
  (excluding the O(2^(N - 1) * N) output space).
"""

from typing import List


def all_paths_source_target(graph: List[List[int]]) -> List[List[int]]:
    """
    Find all paths from node 0 to node n - 1 using state-space DFS backtracking.

    Key Invariants & Mechanics:
    1. DAG Property: Because the graph is strictly acyclic, cycles are impossible.
       No visited set is required to prevent infinite loops.
    2. Symmetrical Backtracking: A single mutable list `path` is passed down the
       recursion tree. Symmetrical append and pop operations eliminate intermediate
       list allocations during traversal.
    3. Terminal Condition: When `node == n - 1`, a snapshot copy `path[:]` is added
       to `result`.
    """
    n = len(graph)
    result: List[List[int]] = []
    path: List[int] = [0]

    def dfs(node: int) -> None:
        if node == n - 1:
            result.append(path[:])
            return

        for neighbor in graph[node]:
            path.append(neighbor)
            dfs(neighbor)
            path.pop()

    dfs(0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def all_paths_source_target(self, graph: List[List[int]]) -> List[List[int]]:
        return all_paths_source_target(graph)
