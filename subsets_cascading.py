"""
LeetCode 78: Subsets (Iterative Cascading Paradigm)
https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

Complexity:
- Time: O(N * 2^N) where N is the length of nums. Starts with 1 subset ([]), doubling
  the number of subsets with each element processed. Adding an element to 2^k existing
  subsets takes O(N) copy time per subset.
- Space: O(1) auxiliary space beyond the output list. Operates iteratively without
  recursion call stack frames.
"""

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    """
    Generate the power set using iterative cascading (breadth-first set expansion).

    Key Invariants & Mechanics:
    1. Base Case: Initialize `result = [[]]`.
    2. Dynamic Expansion: For each integer `num` in `nums`, duplicate all existing
       subsets in `result` and append `num` to each new copy.
    3. Pythonic Acceleration: In Python, list comprehensions and bulk list extensions
       execute in optimized C-loops inside CPython, significantly reducing bytecode
       dispatch overhead compared to recursive function frames.
    """
    result: List[List[int]] = [[]]
    for num in nums:
        result += [curr + [num] for curr in result]
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def subsets(self, nums: List[int]) -> List[List[int]]:
        return subsets(nums)
