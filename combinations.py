"""
LeetCode 77: Combinations
https://leetcode.com/problems/combinations/

Given two integers n and k, return all possible combinations of k numbers chosen
from the range [1, n]. You may return the answer in any order.

Constraints:
- 1 <= n <= 20
- 1 <= k <= n

Complexity:
- Time: O(C(n, k) * k) where C(n, k) = n! / (k! * (n - k)!) is the number of combinations.
  With branch pruning, the recursion explores zero dead branches that lack enough remaining
  elements to complete a combination of size k.
- Space: O(k) auxiliary recursion stack space for the active combination path
  (excluding the O(C(n, k) * k) output space).
"""

from typing import List


def combine(n: int, k: int) -> List[List[int]]:
    """
    Generate all k-combinations from 1..n using pruned state-space backtracking.

    Key Invariants & Mechanics:
    1. Forward-Only Progression: Advancing from `i + 1` preserves strictly ascending order,
       preventing permutations and duplicate combinations.
    2. Combinatorial Branch Pruning:
       - Elements currently chosen: `len(current)`.
       - Elements still needed: `k - len(current)`.
       - To have at least `k - len(current)` integers remaining from `i` to `n`, we require:
             n - i + 1 >= k - len(current)
         Solving for i gives:
             i <= n - (k - len(current)) + 1
       - Any branch with i exceeding this bound can never reach size k and is pruned immediately.
    3. In-Place Path Tracking: Symmetrical append/pop on `current` eliminates intermediate list
       allocations across internal recursion nodes.
    """
    if k <= 0 or k > n:
        return []

    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int) -> None:
        if len(current) == k:
            result.append(current[:])
            return

        # Pruned search boundary: do not branch if remaining candidates < needed
        upper_limit = n - (k - len(current)) + 1
        for i in range(start, upper_limit + 1):
            current.append(i)
            backtrack(i + 1)
            current.pop()

    backtrack(1)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combine(self, n: int, k: int) -> List[List[int]]:
        return combine(n, k)
