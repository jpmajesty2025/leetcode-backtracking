"""
LeetCode 131: Palindrome Partitioning (Bottom-Up Iterative Dynamic Programming)
https://leetcode.com/problems/palindrome-partitioning/

Given a string s, partition s such that every substring of the partition is a
palindrome. Return all possible palindrome partitioning of s.

Constraints:
- 1 <= s.length <= 16
- s contains only lowercase English letters.

Complexity:
- Time: O(N^2 + 2^N * N). Populates palindrome DP table in O(N^2), then builds
  all partitions iteratively layer-by-layer up to s[:N].
- Space: O(2^N * N) to store the prefix partition lists in dp table.
"""

from typing import List


def partition(s: str) -> List[List[str]]:
    """
    Generate all palindrome partitionings iteratively using bottom-up DP.

    Key Invariants & Mechanics:
    1. 2D Palindrome Table:
       Precomputes `is_pal[j][i - 1]` to determine if `s[j:i]` is a palindrome in O(1).
    2. Prefix DP Accumulator:
       Let `dp[i]` contain all valid palindrome partitionings of the prefix `s[:i]`.
       Base case: `dp[0] = [[]]` (empty prefix has one empty partition).
    3. State Transition:
       For each boundary `i` from 1 to n:
         For each split point `j` from 0 to i - 1:
           If `is_pal[j][i - 1]`:
             Extend each previous partition `p` in `dp[j]` with `s[j:i]` and add to `dp[i]`.
    4. Zero Recursion Overhead:
       Runs completely iteratively without recursion call stack or backtracking unwinding.
    """
    if not s:
        return []

    n = len(s)
    is_pal: List[List[bool]] = [[False] * n for _ in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    dp: List[List[List[str]]] = [[] for _ in range(n + 1)]
    dp[0] = [[]]

    for i in range(1, n + 1):
        for j in range(i):
            if is_pal[j][i - 1]:
                sub = s[j:i]
                for prev in dp[j]:
                    dp[i].append(prev + [sub])

    return dp[n]


class Solution:
    """LeetCode submission interface wrapper."""

    def partition(self, s: str) -> List[List[str]]:
        return partition(s)
