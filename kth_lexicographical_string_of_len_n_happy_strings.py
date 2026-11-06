"""
LeetCode 1415: The k-th Lexicographical String of All Happy Strings of Length n
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
- Time: O(k * n) worst-case time bound. Generates happy strings in lexicographical
  order, halting recursion immediately upon discovering the k-th valid string.
  If k exceeds 3 * 2^(n-1), aborts in O(1) time.
- Space: O(n) auxiliary space for the recursion call stack and mutable path buffer.
"""

from typing import List


def get_happy_string(n: int, k: int) -> str:
    """
    Generate happy strings in lexicographical order using backtracking with early exit.

    Key Invariants & Mechanics:
    1. Early Capacity Guard:
       Total happy strings of length n is exactly 3 * 2^(n - 1).
       If k <= 0 or k > 3 * 2^(n - 1), return "" in O(1) time.
    2. In-Place Path Buffer:
       Use a mutable list `path` with push/pop operations rather than repeated string
       allocations, keeping auxiliary memory to O(n).
    3. Immediate Short-Circuit Termination:
       A leaf counter tracks completed strings of length n. As soon as count reaches k,
       the search halts and immediately unwinds the call stack without exploring
       subsequent branches.
    """
    if n <= 0 or k <= 0:
        return ""

    total_possible = 3 * (1 << (n - 1))
    if k > total_possible:
        return ""

    count = 0
    result = ""
    path: List[str] = []

    def backtrack() -> bool:
        nonlocal count, result
        if len(path) == n:
            count += 1
            if count == k:
                result = "".join(path)
                return True
            return False

        for char in ("a", "b", "c"):
            if not path or path[-1] != char:
                path.append(char)
                if backtrack():
                    return True
                path.pop()

        return False

    backtrack()
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def getHappyString(self, n: int, k: int) -> str:
        return get_happy_string(n, k)
