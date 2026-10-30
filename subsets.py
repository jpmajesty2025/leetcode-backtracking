"""
LeetCode 78: Subsets
https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

Complexity:
- Time: O(N * 2^N) where N is the length of nums. The power set contains 2^N subsets,
  with an average subset length of N / 2. Copying subsets into the result takes O(N)
  work per state.
- Space: O(N) auxiliary space for the recursion call stack (excluding the O(N * 2^N)
  output space).
"""

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    """
    Generate the power set using state-space combination-tree backtracking.

    Key Invariants & Mechanics:
    1. Combination Tree Exploration: At each recursion frame, the candidate path `current`
       represents a valid subset and is cloned into `result`.
    2. Forward-Only Indexing: The loop advances strictly from `start` to `len(nums) - 1`,
       ensuring that each subset is generated with strictly increasing indices, eliminating
       permutations and duplicate subsets.
    3. In-Place State Mutation: Symmetrical `append` and `pop` maintain the active path
       in a single reusable list, avoiding intermediate list concatenations.
    """
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int) -> None:
        result.append(current[:])
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1)
            current.pop()

    backtrack(0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def subsets(self, nums: List[int]) -> List[List[int]]:
        return subsets(nums)
