"""
LeetCode 39: Combination Sum (Binary Choice State Tree)
https://leetcode.com/problems/combination-sum/

Given an array of distinct integers candidates and a target integer target, return
a list of all unique combinations of candidates where the chosen numbers sum to target.

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct.
- 1 <= target <= 40

Complexity:
- Time: O(2^(T/M)) binary branching bound, where T is target and M is min candidate.
  Branches where candidate exceeds remaining target are pruned immediately.
- Space: O(T/M) auxiliary recursion stack space.
"""

from typing import List


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all unique combinations summing to target using a binary choice tree (Include / Exclude).

    Key Invariants & Mechanics:
    1. Binary Branching: At each state `(index, remain)`:
       - Choice 1 (Include): Pick `candidates[index]`. Because elements may be reused,
         recurse with the SAME `index` and decremented `remain - candidates[index]`.
       - Choice 2 (Exclude): Skip `candidates[index]` permanently for this path by
         recursing to `index + 1` with unchanged `remain`.
    2. Pruning: Sorting candidates upfront allows pruning when `cands[index] > remain`.
    3. Structural Clarity: Avoids loop iteration inside recursion frames by expressing
       the recurrence as a strict binary decision tree.
    """
    if target <= 0 or not candidates:
        return []

    cands = sorted(candidates)
    result: List[List[int]] = []
    current: List[int] = []
    n = len(cands)

    def dfs(index: int, remain: int) -> None:
        if remain == 0:
            result.append(current[:])
            return

        if index == n or cands[index] > remain:
            return

        # Choice 1: Include cands[index] (stay at index for unlimited reuse)
        current.append(cands[index])
        dfs(index, remain - cands[index])
        current.pop()

        # Choice 2: Exclude cands[index] (advance to next candidate)
        dfs(index + 1, remain)

    dfs(0, target)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combination_sum(self, candidates: List[int], target: int) -> List[List[int]]:
        return combination_sum(candidates, target)
