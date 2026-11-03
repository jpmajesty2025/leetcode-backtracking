"""
LeetCode 216: Combination Sum III
https://leetcode.com/problems/combination-sum-iii/

Find all valid combinations of k numbers that sum up to n such that the following
conditions are true:
- Only numbers 1 through 9 are used.
- Each number is used at most once.

Return a list of all possible valid combinations. The list must not contain the same
combination twice, and the combinations may be returned in any order.

Constraints:
- 2 <= k <= 9
- 1 <= n <= 60

Complexity:
- Time: O(C(9, k) * k). Since choices are strictly drawn from {1..9}, the search space
  is bounded by at most C(9, k) combinations (at most C(9, 4) = 126 nodes at depth k).
  With double-ended arithmetic pruning, impossible branches are aborted before evaluation.
- Space: O(k) auxiliary recursion stack space for the active combination path
  (excluding output space).
"""

from typing import List


def combination_sum_3(k: int, n: int) -> List[List[int]]:
    """
    Find all combinations of k distinct digits (1..9) summing to n using pruned backtracking.

    Key Invariants & Mechanics:
    1. Global Feasibility Envelope:
       The minimal achievable sum of k distinct digits is:
           min_sum = k * (k + 1) // 2  (sum of 1..k)
       The maximal achievable sum of k distinct digits is:
           max_sum = k * (19 - k) // 2  (sum of (10-k)..9)
       If n < min_sum or n > max_sum, return [] in O(1) without touching recursion.
    2. Dynamic Branch Bound:
       To select `rem_k` more digits from `[i, 9]`, we must have at least `rem_k` candidates:
           9 - i + 1 >= rem_k  ==>  i <= 9 - rem_k + 1
       Combining with the remainder sum constraint gives:
           upper_limit = min(9 - rem_k + 1, rem_sum)
    3. Double-Ended Capacity Pruning:
       At any recursive frame, if `rem_sum` falls outside the achievable [min_sum, max_sum]
       window of the remaining candidate pool, the subtree is pruned immediately.
    4. Symmetrical In-Place Mutation:
       `current` is mutated in-place via append/pop, avoiding intermediate list churn.
    """
    # Global boundary check
    min_possible = k * (k + 1) // 2
    max_possible = k * (19 - k) // 2
    if k <= 0 or k > 9 or n < min_possible or n > max_possible:
        return []

    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int, rem_sum: int, rem_k: int) -> None:
        if rem_k == 0:
            if rem_sum == 0:
                result.append(current[:])
            return

        # Double-ended capacity pruning:
        # Min achievable sum using rem_k numbers starting from 'start'
        min_rem = rem_k * (2 * start + rem_k - 1) // 2
        # Max achievable sum using the largest rem_k numbers in [start, 9]
        max_rem = rem_k * (19 - rem_k) // 2
        if rem_sum < min_rem or rem_sum > max_rem:
            return

        upper_limit = min(9 - rem_k + 1, rem_sum)
        for i in range(start, upper_limit + 1):
            current.append(i)
            backtrack(i + 1, rem_sum - i, rem_k - 1)
            current.pop()

    backtrack(1, n, k)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        return combination_sum_3(k, n)
