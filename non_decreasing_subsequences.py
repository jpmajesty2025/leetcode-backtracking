"""
LeetCode 491: Non-decreasing Subsequences
https://leetcode.com/problems/non-decreasing-subsequences/

Given an integer array nums, return all the different possible non-decreasing
subsequences of the given array with at least two elements. You may return the
answer in any order.

Constraints:
- 1 <= nums.length <= 15
- -100 <= nums[i] <= 100

Complexity:
- Time: O(2^N * N) worst case, where N is nums.length. With pruning for non-decreasing
  order and level-wise sibling deduplication, the actual search tree is significantly
  smaller than 2^N.
- Space: O(N) auxiliary space for the recursion call stack and mutable path buffer
  (excluding the space required to return the output list).
"""

from typing import List


def find_subsequences(nums: List[int]) -> List[List[int]]:
    """
    Find all non-decreasing subsequences of length >= 2 using backtracking.

    Key Invariants & Mechanics:
    1. Subsequence Preservation (No Sorting):
       Unlike Subsets II or Combination Sum II, the array `nums` CANNOT be sorted
       because sorting destroys the original relative ordering of elements.
    2. Level-Wise Sibling Deduplication:
       To prevent duplicate subsequences without sorting, each recursion frame uses
       a `used` set to record values already branched on at the current depth.
       If the same number appears multiple times in `nums[start:]`, only its first
       occurrence at this level is explored.
    3. Direct List Collection:
       Because level-wise deduplication mathematically guarantees that every
       generated subsequence is unique, we can directly append `path[:]` to `result`
       without paying the overhead of tuple hashing, set deduplication, and
       post-conversion.
    """
    if not nums or len(nums) < 2:
        return []

    result: List[List[int]] = []
    path: List[int] = []
    n = len(nums)

    def backtrack(start: int) -> None:
        if len(path) >= 2:
            result.append(path[:])

        used = set()
        for i in range(start, n):
            val = nums[i]
            # Prune strictly decreasing transitions and duplicate sibling branches
            if (not path or val >= path[-1]) and val not in used:
                used.add(val)
                path.append(val)
                backtrack(i + 1)
                path.pop()

    backtrack(0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        return find_subsequences(nums)
