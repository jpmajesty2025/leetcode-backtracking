"""
LeetCode 131: Palindrome Partitioning
https://leetcode.com/problems/palindrome-partitioning/

Given a string s, partition s such that every substring of the partition is a
palindrome. Return all possible palindrome partitioning of s.

Constraints:
- 1 <= s.length <= 16
- s contains only lowercase English letters.

Complexity:
- Time: O(2^N * N) worst case, where N is s.length. A string of length N has 2^(N - 1)
  possible partitions. In the worst case (e.g. "aaaa"), every partition is valid
  and takes O(N) time to copy.
- Space: O(N) auxiliary space for the recursion call stack and mutable path buffer
  (excluding output list).
"""

from typing import List


def partition(s: str) -> List[List[str]]:
    """
    Generate all palindrome partitionings of s using backtracking.

    Key Invariants & Mechanics:
    1. Base Case:
       When `start == len(s)`, all characters have been cleanly partitioned into
       palindromes; append a shallow copy of `path` to `result`.
    2. Candidate Exploration:
       For each index `end` from `start + 1` to `len(s) + 1`, slice `substring = s[start:end]`.
       If `substring` is a palindrome (`substring == substring[::-1]`), append it to `path`,
       recurse on remaining suffix starting at `end`, then backtrack by popping.
    3. Memory Management:
       Uses an in-place mutable `path` buffer rather than creating new lists on every branch.
    """
    if not s:
        return []

    result: List[List[str]] = []
    path: List[str] = []
    n = len(s)

    def is_palindrome(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start: int) -> None:
        if start == n:
            result.append(path[:])
            return

        for end in range(start + 1, n + 1):
            substring = s[start:end]
            if is_palindrome(substring):
                path.append(substring)
                backtrack(end)
                path.pop()

    backtrack(0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def partition(self, s: str) -> List[List[str]]:
        return partition(s)
