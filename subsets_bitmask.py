"""
LeetCode 78: Subsets (Bitmask Enumeration Paradigm)
https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

Complexity:
- Time: O(N * 2^N) where N is the length of nums. Loops through 2^N integer masks. For each
  mask, inspecting all N bits takes O(N) time.
- Space: O(1) auxiliary space beyond the output list. Iterates sequentially without
  recursion call stack frames or dynamic heap buffers.
"""


def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate the power set using binary bitmask enumeration.

    Key Invariants & Mechanics:
    1. Bijection: There exists a direct 1-to-1 bijection between the 2^N subsets of an
       N-element set and the binary representations of integers in [0, 2^N - 1].
    2. Bit Testing: The j-th bit of integer `mask` indicates whether `nums[j]` is
       present in the corresponding subset:
       - If `(mask >> j) & 1 == 1`, include `nums[j]`.
       - If `(mask >> j) & 1 == 0`, exclude `nums[j]`.
    3. Memory Overhead: Requires zero call stack memory and zero auxiliary state arrays.
    """
    n = len(nums)
    total_subsets = 1 << n
    result: list[list[int]] = []

    for mask in range(total_subsets):
        subset: list[int] = []
        for j in range(n):
            if (mask >> j) & 1:
                subset.append(nums[j])
        result.append(subset)

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def subsets(self, nums: list[int]) -> list[list[int]]:
        return subsets(nums)
