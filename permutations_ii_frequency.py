"""
LeetCode 47: Permutations II (Frequency Map / Counter Paradigm)
https://leetcode.com/problems/permutations-ii/

Given a collection of numbers, nums, that might contain duplicates, return all possible
unique permutations in any order.

Complexity:
- Time: O(P * N), where P is the number of unique permutations.
- Space: O(U) auxiliary space for the frequency map (where U <= N is distinct elements)
  plus O(N) recursion call stack depth.
"""

from collections import Counter
from typing import List


def permute_unique(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations using a character/number frequency map.

    Key Invariants & Mechanics:
    1. Multi-set Frequency Abstraction:
       Instead of tracking boolean indices `used[i]` across repeated values in an array,
       compress `nums` into distinct values and their counts via `Counter(nums)`.
    2. Zero Duplicate Branches by Construction:
       The branch loop iterates over `counts.keys()`. Because each distinct value appears
       in the loop exactly ONCE, sibling branches at the same depth never choose duplicate
       values. No `arr[i] == arr[i - 1]` checks are required!
    3. Decrement / Increment Backtracking:
       Temporarily decrement `counts[num]` when entering a branch and restore it on exit.
    """
    if not nums:
        return []

    result: List[List[int]] = []
    current: List[int] = []
    counts = Counter(nums)
    n = len(nums)

    def backtrack() -> None:
        if len(current) == n:
            result.append(current[:])
            return

        for num in counts:
            if counts[num] > 0:
                counts[num] -= 1
                current.append(num)
                backtrack()
                current.pop()
                counts[num] += 1

    backtrack()
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        return permute_unique(nums)
