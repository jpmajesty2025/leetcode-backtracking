"""
LeetCode 1415: The k-th Lexicographical String of All Happy Strings of Length n
(Iterative BFS / Queue Level-Order Generation)
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
- Time: O(k * n) time. Expands candidates level-by-level in strict lexicographical order,
  stopping as soon as the k-th string of length n is dequeued.
- Space: O(k * n) space in the BFS queue frontier.
"""

from collections import deque
from typing import Deque


def get_happy_string(n: int, k: int) -> str:
    """
    Generate happy strings iteratively using BFS queue expansion.

    Key Invariants & Mechanics:
    1. Early Capacity Guard:
       Total happy strings of length n is exactly 3 * 2^(n - 1).
       If k <= 0 or k > 3 * 2^(n - 1), return "" in O(1) time.
    2. FIFO Queue Ordering:
       Initial queue: ["a", "b", "c"].
       Because characters are enqueued in alphabetical order, strings of any length
       are popped in strictly ascending lexicographical order.
    3. Early Termination:
       A leaf counter tracks dequeued strings of length n. When count == k, return
       the string immediately without further expansions.
    """
    if n <= 0 or k <= 0:
        return ""

    total_possible = 3 * (1 << (n - 1))
    if k > total_possible:
        return ""

    queue: Deque[str] = deque(["a", "b", "c"])
    count = 0

    while queue:
        curr = queue.popleft()
        if len(curr) == n:
            count += 1
            if count == k:
                return curr
        else:
            last_char = curr[-1]
            for next_char in ("a", "b", "c"):
                if next_char != last_char:
                    queue.append(curr + next_char)

    return ""


class Solution:
    """LeetCode submission interface wrapper."""

    def getHappyString(self, n: int, k: int) -> str:
        return get_happy_string(n, k)
