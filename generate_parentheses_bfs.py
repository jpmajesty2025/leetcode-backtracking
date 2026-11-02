"""
LeetCode 22: Generate Parentheses (BFS Queue Level-Order Expansion)
https://leetcode.com/problems/generate-parentheses/

Given n pairs of parentheses, write a function to generate all combinations
of well-formed parentheses.

Constraints:
- 1 <= n <= 8

Complexity:
- Time: O(4^n / sqrt(n)) asymptotically, matching the n-th Catalan number C_n.
- Space: O(4^n / sqrt(n)) auxiliary memory in the queue at maximum breadth.
"""

from collections import deque
from typing import List, Tuple


def generate_parenthesis(n: int) -> List[str]:
    """
    Generate all valid combinations using BFS level-order queue expansion.

    Key Invariants & Mechanics:
    1. Queue State: Each item is a 3-tuple `(current_prefix, open_count, close_count)`.
    2. Pruned Expansion:
       - If `open_count < n`: enqueue `(current + '(', open_count + 1, close_count)`.
       - If `close_count < open_count`: enqueue `(current + ')', open_count, close_count + 1)`.
    3. Non-Recursive Execution: Operates iteratively on the heap, eliminating recursion
       call stack frames.
    """
    if n <= 0:
        return []

    result: List[str] = []
    queue: deque[Tuple[str, int, int]] = deque([("", 0, 0)])

    while queue:
        curr, open_c, close_c = queue.popleft()

        if len(curr) == 2 * n:
            result.append(curr)
            continue

        if open_c < n:
            queue.append((curr + "(", open_c + 1, close_c))

        if close_c < open_c:
            queue.append((curr + ")", open_c, close_c + 1))

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def generateParenthesis(self, n: int) -> List[str]:
        return generate_parenthesis(n)
