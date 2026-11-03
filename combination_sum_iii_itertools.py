"""
LeetCode 216: Combination Sum III (Itertools Combinations Engine)
https://leetcode.com/problems/combination-sum-iii/

Find all valid combinations of k numbers that sum up to n such that:
- Only numbers 1 through 9 are used.
- Each number is used at most once.

Complexity:
- Time: O(C(9, k) * k). Built-in C implementation enumerates at most C(9, 4) = 126 combinations.
- Space: O(1) auxiliary space beyond the output list.
"""

import itertools
from typing import List


def combination_sum_3(k: int, n: int) -> List[List[int]]:
    """
    Find all valid combinations using C-accelerated itertools.combinations.

    Key Invariants & Mechanics:
    1. Direct Generation: `itertools.combinations(range(1, 10), k)` directly generates
       all subsets of size k in strictly increasing order without duplicates.
    2. Zero Branching Overhead: Executes combination enumeration in compiled C.
    3. Filter: Keep only combinations whose sum equals `n`.
    """
    min_possible = k * (k + 1) // 2
    max_possible = k * (19 - k) // 2
    if k <= 0 or k > 9 or n < min_possible or n > max_possible:
        return []

    return [list(comb) for comb in itertools.combinations(range(1, 10), k) if sum(comb) == n]


class Solution:
    """LeetCode submission interface wrapper."""

    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        return combination_sum_3(k, n)
