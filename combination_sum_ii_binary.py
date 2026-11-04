"""
LeetCode 40: Combination Sum II (Binary Decision Tree - Include / Exclude with Twin Skipping)
https://leetcode.com/problems/combination-sum-ii/

Given a collection of candidate numbers (candidates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sum to target.

Complexity:
- Time: O(2^N) upper bound. Pruned binary branching tree.
- Space: O(N) auxiliary recursion call stack space.
"""

from typing import List


def combination_sum_2(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all unique combinations using a binary decision tree (Include / Exclude).

    Key Invariants & Mechanics:
    1. Binary Choice Structure:
       At state `(index, remaining)`:
       - Choice 1 (Include): Pick `cands[index]`. Recurse with `index + 1` (single use)
         and `remaining - cands[index]`.
       - Choice 2 (Exclude): Skip `cands[index]` AND all its identical consecutive twins!
         Find the next index `next_idx` where `cands[next_idx] != cands[index]`.
         Recurse with `(next_idx, remaining)`.
    2. Zero Duplicate Branches by Construction:
       Skipping all identical elements during the Exclude choice guarantees that we never
       evaluate another subtree with the same element skipped at this decision point.
    3. Structural Clarity: Eliminates internal loops inside the recursive function.
    """
    if target <= 0 or not candidates:
        return []

    cands = sorted(candidates)
    n = len(cands)
    result: List[List[int]] = []
    current: List[int] = []

    def dfs(index: int, remaining: int) -> None:
        if remaining == 0:
            result.append(current[:])
            return

        if index == n or cands[index] > remaining:
            return

        # Choice 1: Include cands[index]
        current.append(cands[index])
        dfs(index + 1, remaining - cands[index])
        current.pop()

        # Choice 2: Exclude cands[index] and skip all identical duplicates
        next_index = index + 1
        while next_index < n and cands[next_index] == cands[index]:
            next_index += 1

        dfs(next_index, remaining)

    dfs(0, target)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        return combination_sum_2(candidates, target)
