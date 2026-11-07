"""
LeetCode 491: Non-decreasing Subsequences (Iterative Dynamic Programming / Prefix Extension)
https://leetcode.com/problems/non-decreasing-subsequences/

Given an integer array nums, return all the different possible non-decreasing
subsequences of the given array with at least two elements. You may return the
answer in any order.

Constraints:
- 1 <= nums.length <= 15
- -100 <= nums[i] <= 100

Complexity:
- Time: O(2^N * N) worst case, where N is nums.length. Builds unique subsequences
  incrementally by extending existing valid chains with each incoming element.
- Space: O(2^N * N) to store the set of generated subsequence tuples during execution.
"""

from typing import List, Set, Tuple


def find_subsequences(nums: List[int]) -> List[List[int]]:
    """
    Find all non-decreasing subsequences using iterative prefix extension.

    Key Invariants & Mechanics:
    1. Bottom-Up Chain Expansion:
       Iterate through each number `x` in `nums`. Every previously established
       subsequence `seq` whose last element satisfies `seq[-1] <= x` can be extended
       into a new valid non-decreasing subsequence `seq + (x,)`.
    2. Singleton Seed Generation:
       The singleton tuple `(x,)` is added as a seed for subsequent extensions.
    3. Natural Deduplication:
       By maintaining accumulated chains in a Python set of tuples, duplicate
       subsequences formed from repeated elements are automatically deduplicated
       without recursion or index manipulation.
    4. Filtering:
       At termination, filter out singletons (`len >= 2`) and convert tuples to lists.
    """
    if not nums or len(nums) < 2:
        return []

    chains: Set[Tuple[int, ...]] = set()

    for x in nums:
        # Extend all valid existing chains and register singleton (x,)
        chains |= {seq + (x,) for seq in chains if seq[-1] <= x} | {(x,)}

    return [list(seq) for seq in chains if len(seq) >= 2]


class Solution:
    """LeetCode submission interface wrapper."""

    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        return find_subsequences(nums)
