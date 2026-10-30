"""
LeetCode 797: All Paths From Source to Target (Memoized DFS / DP on DAG)
https://leetcode.com/problems/all-paths-from-source-to-target/

Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all
possible paths from node 0 to node n - 1 and return them in any order.

Constraints:
- n == graph.length
- 2 <= n <= 15
- 0 <= graph[i][j] < n
- graph[i][j] != i (no self-loops)
- All the elements of graph[i] are unique.
- The input graph is guaranteed to be a DAG.

Complexity:
- Time: O(2^(N - 1) * N) worst case for dense DAGs. Solves each subproblem `paths_from(u)`
  and reuses the result across multiple incoming edges.
- Space: O(2^(N - 1) * N) auxiliary memory in the memoization table storing suffix
  paths for intermediate nodes.
"""

from typing import Dict, List


def all_paths_source_target(graph: List[List[int]]) -> List[List[int]]:
    """
    Find all paths from node 0 to node n - 1 using top-down memoized DFS (DP on DAG).

    Key Invariants & Mechanics:
    1. Subproblem Definition: `dfs(node)` returns all suffix paths from `node` to `n - 1`.
    2. Overlapping Subproblems: In a DAG with multiple paths converging on intermediate
       nodes, `dfs(node)` is computed once and cached in `memo`.
    3. Recombination: For each neighbor `v` of `node`, prefix `node` to each path returned
       by `dfs(v)`.
    """
    n = len(graph)
    memo: Dict[int, List[List[int]]] = {}

    def dfs(node: int) -> List[List[int]]:
        if node in memo:
            return memo[node]

        if node == n - 1:
            return [[n - 1]]

        paths: List[List[int]] = []
        for neighbor in graph[node]:
            for suffix in dfs(neighbor):
                paths.append([node] + suffix)

        memo[node] = paths
        return paths

    return dfs(0)


class Solution:
    """LeetCode submission interface wrapper."""

    def all_paths_source_target(self, graph: List[List[int]]) -> List[List[int]]:
        return all_paths_source_target(graph)
