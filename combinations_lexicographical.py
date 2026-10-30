"""
LeetCode 77: Combinations (Iterative Lexicographical Generation)
https://leetcode.com/problems/combinations/

Given two integers n and k, return all possible combinations of k numbers chosen
from the range [1, n]. You may return the answer in any order.

Constraints:
- 1 <= n <= 20
- 1 <= k <= n

Complexity:
- Time: O(C(n, k) * k) where C(n, k) = n! / (k! * (n - k)!). Each combination takes
  O(k) time to copy and advance to the next state in lexicographical order.
- Space: O(1) auxiliary space beyond the output list. Operates iteratively without
  call stack frames or recursive overhead.
"""

from typing import List


def combine(n: int, k: int) -> List[List[int]]:
    """
    Generate all k-combinations from 1..n iteratively in lexicographical order.

    Key Invariants & Mechanics (Next Combination / Knuth Algorithm T):
    1. Initial State: Start with the lexicographical minimum combination: [1, 2, ..., k].
    2. Upper Bound Condition: At position j (0-indexed, 0 <= j < k), the maximum possible
       value that allows filling subsequent positions up to n is:
           max_val(j) = n - k + j + 1
    3. State Transition:
       a. Scan from right to left (j = k - 1 down to 0) to find the rightmost position
          where curr[j] < max_val(j).
       b. Increment curr[j] by 1.
       c. Reset all subsequent positions m in [j + 1, k - 1] to curr[m] = curr[m - 1] + 1.
       d. When no such j exists (j < 0), all combinations have been enumerated.
    4. Eliminates call stack frames entirely, guaranteeing O(1) auxiliary memory.
    """
    if k <= 0 or k > n:
        return []

    result: List[List[int]] = []
    curr = list(range(1, k + 1))
    result.append(curr[:])

    while True:
        # Step 1: Find the rightmost index that has not reached its maximum value
        j = k - 1
        while j >= 0 and curr[j] == n - k + j + 1:
            j -= 1

        if j < 0:
            break

        # Step 2: Increment pivot element
        curr[j] += 1

        # Step 3: Reset trailing elements to minimal valid sequence
        for m in range(j + 1, k):
            curr[m] = curr[m - 1] + 1

        result.append(curr[:])

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combine(self, n: int, k: int) -> List[List[int]]:
        return combine(n, k)
