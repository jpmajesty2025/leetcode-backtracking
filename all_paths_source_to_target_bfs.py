"""
LeetCode 797: All Paths From Source to Target (BFS Path Queue)
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
- Time: O(2^(N - 1) * N) worst case for dense DAGs. Breadth-first level-by-level
  expansion discovers paths in increasing order of hop count.
- Space: O(2^(N - 1) * N) auxiliary memory in the BFS queue, holding frontier paths
  at the widest level of the DAG traversal.
"""

from collections import deque
from typing import List


def all_paths_source_target(graph: List[List[int]]) -> List[List[int]]:
    """
    Find all paths from node 0 to node n - 1 using breadth-first search (BFS).

    Key Invariants & Mechanics:
    1. Queue of Paths: Each item in the deque is a complete path prefix `[0, ..., u]`.
    2. Level-Order Expansion: Popping the leftmost path and appending valid outgoing
       neighbors produces paths grouped naturally by hop length.
    3. Non-Recursive Execution: Completely avoids recursion frames, eliminating any
       risk of call stack overflow on deep DAG structures.
    """
    n = len(graph)
    result: List[List[int]] = []
    queue: deque[List[int]] = deque([[0]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == n - 1:
            result.append(path)
            continue

        for neighbor in graph[node]:
            queue.append(path + [neighbor])

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def all_paths_source_target(self, graph: List[List[int]]) -> List[List[int]]:
        return all_paths_source_target(graph)
