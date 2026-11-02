"""
LeetCode 22: Generate Parentheses
https://leetcode.com/problems/generate-parentheses/

Given n pairs of parentheses, write a function to generate all combinations
of well-formed parentheses.

Constraints:
- 1 <= n <= 8

Complexity:
- Time: O(4^n / sqrt(n)) asymptotically. The number of valid combinations is the
  n-th Catalan number C_n = (1 / (n + 1)) * comb(2n, n) ~ 4^n / (n^(3/2) * sqrt(pi)).
  Since each valid sequence has length 2n, generating all combinations takes
  O(2n * C_n) = O(4^n / sqrt(n)) time.
- Space: O(n) auxiliary recursion call stack space (excluding the output list).
"""

from typing import List


def generate_parenthesis(n: int) -> List[str]:
    """
    Generate all valid combinations of n pairs of parentheses using state-space DFS.

    Key Invariants & Mechanics:
    1. Balance Condition: A parenthesis prefix is valid if and only if:
       - `open_count <= n`: Cannot use more than n opening brackets.
       - `close_count <= open_count`: Cannot close more brackets than have been opened.
    2. Branch Pruning:
       - Only branch to `'('` when `open_count < n`.
       - Only branch to `')'` when `close_count < open_count`.
       This guarantees that every path explored in the recursion tree leads strictly
       to a well-formed parenthesis combination without dead branches.
    3. Terminal State: When `len(current) == 2 * n`, all brackets have been placed.
    """
    if n <= 0:
        return []

    result: List[str] = []

    def backtrack(current: str, open_count: int, close_count: int) -> None:
        if len(current) == 2 * n:
            result.append(current)
            return

        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)

        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)

    backtrack("", 0, 0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def generateParenthesis(self, n: int) -> List[str]:
        return generate_parenthesis(n)
