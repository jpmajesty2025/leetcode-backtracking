"""
LeetCode 131: Palindrome Partitioning (Backtracking with Precomputed DP Table)
https://leetcode.com/problems/palindrome-partitioning/

Given a string s, partition s such that every substring of the partition is a
palindrome. Return all possible palindrome partitioning of s.

Constraints:
- 1 <= s.length <= 16
- s contains only lowercase English letters.

Complexity:
- Time: O(N^2 + 2^N * N). Precomputing the NxN palindrome table takes O(N^2) time.
  During backtracking, each palindrome verification takes O(1) table lookup time
  instead of O(N) string reversal and comparison.
- Space: O(N^2) for the 2D boolean palindrome table + O(N) recursion stack.
"""

from typing import List


def partition(s: str) -> List[List[str]]:
    """
    Generate palindrome partitionings using a precomputed 2D DP palindrome table.

    Key Invariants & Mechanics:
    1. O(N^2) Palindrome Precomputation:
       Let `is_pal[i][j]` denote whether substring s[i:j+1] is a palindrome.
       Transition: `s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1])`.
       Filling bottom-up eliminates all repeated slicing and string reversing.
    2. O(1) Substring Verification:
       During backtracking, checking if s[start:end+1] is a palindrome reduces to
       `is_pal[start][end]`, eliminating substring allocations along invalid branches.
    3. In-Place Recursion:
       Uses a shared `path` buffer with append/pop operations.
    """
    if not s:
        return []

    n = len(s)
    # is_pal[i][j] is True if s[i..j] is a palindrome
    is_pal: List[List[bool]] = [[False] * n for _ in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    result: List[List[str]] = []
    path: List[str] = []

    def backtrack(start: int) -> None:
        if start == n:
            result.append(path[:])
            return

        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start : end + 1])
                backtrack(end + 1)
                path.pop()

    backtrack(0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def partition(self, s: str) -> List[List[str]]:
        return partition(s)
