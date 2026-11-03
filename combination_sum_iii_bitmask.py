"""
LeetCode 216: Combination Sum III (Bitmask Enumeration Paradigm)
https://leetcode.com/problems/combination-sum-iii/

Find all valid combinations of k numbers that sum up to n such that:
- Only numbers 1 through 9 are used.
- Each number is used at most once.

Complexity:
- Time: O(2^9) = O(512) = O(1). Exactly 512 total subsets exist for digits {1..9}.
  Checking each subset takes O(1) bitwise operations.
- Space: O(1) auxiliary space beyond the output list.
"""

from typing import List


def combination_sum_3(k: int, n: int) -> List[List[int]]:
    """
    Find all valid combinations using bitmask subset filtering.

    Key Invariants & Mechanics:
    1. Finite Power Set: Since numbers are restricted to {1..9}, there are exactly
       2^9 = 512 subsets in total.
    2. Bit Testing:
       Bit j of `mask` (0 <= j < 9) indicates whether integer `j + 1` is chosen.
    3. Filtering Invariants:
       - Hamming weight: `mask.bit_count() == k` (exactly k numbers chosen)
       - Target sum: sum of set bits equals `n`
    4. Non-Recursive Execution: Completely avoids recursion frames and decision trees.
    """
    min_possible = k * (k + 1) // 2
    max_possible = k * (19 - k) // 2
    if k <= 0 or k > 9 or n < min_possible or n > max_possible:
        return []

    result: List[List[int]] = []

    for mask in range(1, 1 << 9):
        if mask.bit_count() == k:
            total = 0
            subset: List[int] = []
            for j in range(9):
                if (mask >> j) & 1:
                    val = j + 1
                    total += val
                    subset.append(val)
                    if total > n:
                        break

            if total == n:
                result.append(subset)

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        return combination_sum_3(k, n)
