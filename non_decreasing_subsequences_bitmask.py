"""
LeetCode 491: Non-decreasing Subsequences (Combinatorial Bitmask Subset Enumeration)
https://leetcode.com/problems/non-decreasing-subsequences/

Given an integer array nums, return all the different possible non-decreasing
subsequences of the given array with at least two elements. You may return the
answer in any order.

Constraints:
- 1 <= nums.length <= 15
- -100 <= nums[i] <= 100

Complexity:
- Time: O(2^N * N) where N is nums.length <= 15. Systematically evaluates all 2^N
  (at most 32,768) subset masks, validating the non-decreasing invariant.
- Space: O(2^N * N) space for the deduplicated set of subsequence tuples.
"""

from typing import List, Set, Tuple


def find_subsequences(nums: List[int]) -> List[List[int]]:
    """
    Find all non-decreasing subsequences via exhaustive bitmask subset enumeration.

    Key Invariants & Mechanics:
    1. Complete Combinatorial Space:
       Because N <= 15, the entire power set size 2^N is bounded by 32,768.
       Each integer mask in [1, 2^N - 1] represents a unique subsequence candidate.
    2. Zero Recursion Overhead:
       Iterates over masks in a flat, iterative loop without call stack overhead
       or backtracking states.
    3. Non-Decreasing Validation:
       For each mask with bit_count >= 2, traverse the set bits from left to right.
       If any element is strictly smaller than its predecessor in the candidate,
       the mask is rejected.
    4. Set Deduplication:
       Valid subsequences are accumulated in a set of tuples to eliminate duplicate
       subsequences arising from duplicate numbers in `nums`.
    """
    n = len(nums)
    if n < 2:
        return []

    seen: Set[Tuple[int, ...]] = set()
    total_masks = 1 << n

    for mask in range(1, total_masks):
        # A valid subsequence must have at least two elements
        if mask.bit_count() < 2:
            continue

        candidate: List[int] = []
        is_valid = True

        for i in range(n):
            if (mask >> i) & 1:
                val = nums[i]
                if candidate and val < candidate[-1]:
                    is_valid = False
                    break
                candidate.append(val)

        if is_valid:
            seen.add(tuple(candidate))

    return [list(s) for s in seen]


class Solution:
    """LeetCode submission interface wrapper."""

    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        return find_subsequences(nums)
