"""
LeetCode 1415: The k-th Lexicographical String of All Happy Strings of Length n
(Direct Combinatorial / Radix Math Construction)
https://leetcode.com/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/

A happy string is a string that:
- consists only of letters of the set ['a', 'b', 'c'].
- s[i] != s[i + 1] for all values of i from 1 to s.length - 1 (1-indexed).

Given two integers n and k, consider a list of all happy strings of length n sorted
in lexicographical order.

Return the kth string of this list or return an empty string if there are less
than k happy strings of length n.

Constraints:
- 1 <= n <= 10
- 1 <= k <= 100

Complexity:
- Time: O(n) deterministic time. Each character position is computed in O(1) time
  using bit shifts and modular arithmetic, bypassing tree search entirely.
- Space: O(n) to construct the result string; O(1) auxiliary space beyond the output.
"""

from typing import List

# Precomputed next-character choices for each preceding character, sorted lexicographically.
NEXT_CHOICES = {
    "a": ("b", "c"),
    "b": ("a", "c"),
    "c": ("a", "b"),
}


def get_happy_string(n: int, k: int) -> str:
    """
    Directly construct the k-th happy string in O(n) time using radix / binary partitioning.

    Key Invariants & Mechanics:
    1. Complete Regular Tree Structure:
       - The search space consists of 3 root branches ('a', 'b', 'c').
       - Every subsequent level has branching factor exactly 2.
       - Each branch at depth i has exactly 2^(n - 1 - i) descendant leaves.
    2. Zero-Indexed Radix Division:
       - Convert k to 0-based index: `idx = k - 1`.
       - If k <= 0 or k > 3 * 2^(n - 1), return "" immediately.
       - First character: `choice = idx // 2^(n - 1)` from ('a', 'b', 'c').
       - For i = 1 .. n-1:
         `choice = (idx // 2^(n - 1 - i))` selects between the 2 available letters.
         `idx %= 2^(n - 1 - i)` advances to the child subtree offset.
    3. Scalability:
       Unlike backtracking, this method scales effortlessly up to n = 60 without any
       recursion stack or state space exploration.
    """
    if n <= 0 or k <= 0:
        return ""

    total_possible = 3 * (1 << (n - 1))
    if k > total_possible:
        return ""

    idx = k - 1
    result: List[str] = []

    # First character has 3 options: 'a', 'b', 'c'
    block_size = 1 << (n - 1)
    first_choice = idx // block_size
    result.append(("a", "b", "c")[first_choice])
    idx %= block_size

    # Remaining n - 1 characters each have 2 options
    for i in range(1, n):
        block_size >>= 1
        choice = idx // block_size
        idx %= block_size
        prev_char = result[-1]
        result.append(NEXT_CHOICES[prev_char][choice])

    return "".join(result)


class Solution:
    """LeetCode submission interface wrapper."""

    def getHappyString(self, n: int, k: int) -> str:
        return get_happy_string(n, k)
