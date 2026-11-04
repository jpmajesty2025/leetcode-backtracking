"""
LeetCode 40: Combination Sum II (Bounded Knapsack Dynamic Programming)
https://leetcode.com/problems/combination-sum-ii/

Given a collection of candidate numbers (candidates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sum to target.

Complexity:
- Time: O(U * target * K), where U is the number of distinct candidate values and K
  is the average number of unique combinations per amount.
- Space: O(target * K) for the DP memoization table of combinations.
"""

from collections import Counter
from typing import List, Set, Tuple


def combination_sum_2(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all unique combinations using bounded knapsack dynamic programming.

    Key Invariants & Mechanics (Bounded 0/1 Knapsack):
    1. Multiset Grouping: Count frequencies of each candidate: `counts = Counter(candidates)`.
       Sort items `(val, freq)` in ascending order.
    2. Outer Loop Over Distinct Values: Processing each distinct value `val` with its available
       multiplicity `freq` in the outer loop guarantees combinations are constructed in
       non-decreasing order, naturally avoiding duplicate permutations.
    3. DP State: `dp[t]` stores all unique combinations (as sorted tuples) summing to `t`.
    4. Base Case: `dp[0] = {()}`.
    5. Non-Recursive Execution: Operates iteratively, completely avoiding recursion stack limits.
    """
    if target <= 0 or not candidates:
        return []

    counts = Counter(candidates)
    items = sorted(counts.items())

    # dp[t] holds a set of sorted tuples summing to t
    dp: List[Set[Tuple[int, ...]]] = [set() for _ in range(target + 1)]
    dp[0].add(())

    for val, freq in items:
        # Create a new table snapshot to avoid unbounded reuse within the same item
        new_dp = [set(s) for s in dp]
        for count in range(1, freq + 1):
            added_sum = count * val
            if added_sum > target:
                break
            tuple_suffix = tuple([val] * count)
            for t in range(added_sum, target + 1):
                prev_t = t - added_sum
                for prev_combo in dp[prev_t]:
                    new_dp[t].add(prev_combo + tuple_suffix)
        dp = new_dp

    return [list(combo) for combo in dp[target]]


class Solution:
    """LeetCode submission interface wrapper."""

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        return combination_sum_2(candidates, target)
