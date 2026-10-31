"""
LeetCode 39: Combination Sum
https://leetcode.com/problems/combination-sum/

Given an array of distinct integers candidates and a target integer target, return
a list of all unique combinations of candidates where the chosen numbers sum to target.
You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two
combinations are unique if the frequency of at least one of the chosen numbers is different.

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct.
- 1 <= target <= 40

Complexity:
- Time: O(N^(T/M + 1)) in the worst-case upper bound, where N is the number of candidates,
  T is target, and M is the minimum candidate value (maximum recursion depth is T/M).
  With sorting and early break pruning, branches where candidate > remaining target
  are immediately aborted without exploring their subtrees.
- Space: O(T/M) auxiliary recursion stack space and path buffer for the deepest path
  (excluding output space).
"""

from typing import List


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all unique combinations summing to target using sorted branch-pruned backtracking.

    Key Invariants & Mechanics:
    1. Sorting Upfront: Sorting `candidates` in ascending order enables early termination:
       once `cands[i] > remaining_target`, all subsequent elements `cands[j]` (j > i)
       are strictly greater and can be pruned immediately with `break`.
    2. Reusable Elements: Recursing with `start = i` allows the current candidate to be
       reused unlimited times while preventing earlier elements (`< i`) from being
       re-selected, eliminating duplicate permutations.
    3. Decrementing Target: Tracking `remain = remain - candidate` eliminates additive
       arithmetic across frames; the base case is simply `remain == 0`.
    4. Symmetrical Backtracking: A single mutable `current` list is modified in-place
       via append/pop, avoiding intermediate list allocations during traversal.
    """
    if target <= 0 or not candidates:
        return []

    cands = sorted(candidates)
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int, remain: int) -> None:
        if remain == 0:
            result.append(current[:])
            return

        for i in range(start, len(cands)):
            val = cands[i]
            # Pruning Guard: candidates are sorted, so any subsequent val > remain
            if val > remain:
                break

            current.append(val)
            backtrack(i, remain - val)
            current.pop()

    backtrack(0, target)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combination_sum(self, candidates: List[int], target: int) -> List[List[int]]:
        return combination_sum(candidates, target)
