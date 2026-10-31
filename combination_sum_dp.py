"""
LeetCode 39: Combination Sum (Bottom-Up DP / Unbounded Knapsack Paradigm)
https://leetcode.com/problems/combination-sum/

Given an array of distinct integers candidates and a target integer target, return
a list of all unique combinations of candidates where the chosen numbers sum to target.

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct.
- 1 <= target <= 40

Complexity:
- Time: O(C * target * K) where C is the number of candidates and K is the average number
  of combinations per subproblem amount. Bottom-up dynamic programming builds combinations
  iteratively without recursion overhead.
- Space: O(target * K) auxiliary table storage for subproblem combinations.
"""

from typing import List


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all unique combinations summing to target using bottom-up dynamic programming.

    Key Invariants & Mechanics (Coin Change / Unbounded Knapsack):
    1. Outer Loop Over Candidates: Iterating through each candidate `c` in the outer loop
       guarantees that combinations are constructed in non-decreasing order of candidates,
       preventing duplicate permutations (e.g. [2, 3] and [3, 2]).
    2. DP State: `dp[t]` stores all valid combinations that sum exactly to `t`.
    3. Base Case: `dp[0] = [[]]` (there is exactly one way to form sum 0: the empty combination).
    4. Transition: For each candidate `c` and each target `t` from `c` to `target`:
       Every combination in `dp[t - c]` extended by `c` forms a valid combination for `t`.
    5. Non-Recursive Execution: Completely avoids recursion frames and call stack limits.
    """
    if target <= 0 or not candidates:
        return []

    cands = sorted(candidates)
    dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
    dp[0] = [[]]

    for c in cands:
        for t in range(c, target + 1):
            for prev_combo in dp[t - c]:
                dp[t].append(prev_combo + [c])

    return dp[target]


class Solution:
    """LeetCode submission interface wrapper."""

    def combination_sum(self, candidates: List[int], target: int) -> List[List[int]]:
        return combination_sum(candidates, target)
