"""
LeetCode 40: Combination Sum II
https://leetcode.com/problems/combination-sum-ii/

Given a collection of candidate numbers (candidates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sum to target.

Each number in candidates may only be used once in the combination.
The solution set must not contain duplicate combinations.

Constraints:
- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30

Complexity:
- Time: O(2^N) upper bound, where N is len(candidates).
  With sorting and duplicate sibling pruning (`i > start and cands[i] == cands[i - 1]`),
  redundant subtrees are pruned at the root, reducing the effective search space to
  the number of unique combinations.
- Space: O(N) auxiliary recursion stack space and path buffer for the deepest branch
  (excluding output list).
"""

from typing import List


def combination_sum_2(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all unique combinations summing to target with single-use elements and duplicate pruning.

    Key Invariants & Mechanics:
    1. Input Non-Mutation: `cands = sorted(candidates)` copies and sorts without mutating
       caller input.
    2. Ascending Order Pruning: Sorting enables immediate break: if `cands[i] > remaining`,
       all subsequent elements `cands[j]` (j > i) are guaranteed to exceed `remaining`.
    3. Sibling Deduplication Invariant:
       Within the loop for a given recursive frame starting at `start`:
       If `i > start and cands[i] == cands[i - 1]`:
           continue
       This enforces that at this depth, the duplicate value `cands[i]` is only chosen ONCE
       (by the first twin at index `start`). Any subsequent duplicate at the same depth is
       skipped, preventing identical sibling subtrees.
    4. Single-Use Consumption: Advancing to `i + 1` in recursive calls ensures each index is
       consumed at most once per path.
    """
    if target <= 0 or not candidates:
        return []

    cands = sorted(candidates)
    n = len(cands)
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(current[:])
            return

        for i in range(start, n):
            val = cands[i]
            # Early break: subsequent candidates are strictly >= val > remaining
            if val > remaining:
                break
            # Deduplication guard: skip duplicate candidates at the same recursion depth
            if i > start and val == cands[i - 1]:
                continue

            current.append(val)
            backtrack(i + 1, remaining - val)
            current.pop()

    backtrack(0, target)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        return combination_sum_2(candidates, target)
