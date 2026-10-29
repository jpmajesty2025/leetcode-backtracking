"""
LeetCode 46: Permutations
https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

Complexity:
- Time: O(N * N!) where N is the length of nums. There are N! permutations, and copying
  each permutation into the result list takes O(N) time. With boolean tracking, each state
  transition takes O(1) time.
- Space: O(N) auxiliary space for the recursion call stack and boolean visited array
  (excluding the O(N * N!) output space).
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations using state-space backtracking with boolean markers.

    Key Invariants & Mechanics:
    1. A boolean array `used` tracks element availability in O(1) time per candidate.
    2. The candidate path `current` is mutated in-place via push/pop, eliminating
       intermediate list allocations on internal decision tree nodes.
    3. At the base case (len(current) == len(nums)), a shallow copy is appended to `result`.
    """
    if not nums:
        return [[]]

    result: List[List[int]] = []
    n = len(nums)
    used = [False] * n
    current: List[int] = []

    def backtrack() -> None:
        if len(current) == n:
            result.append(current[:])
            return

        for i in range(n):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                backtrack()
                current.pop()
                used[i] = False

    backtrack()
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def permute(self, nums: List[int]) -> List[List[int]]:
        return permute(nums)
