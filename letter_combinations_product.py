"""
LeetCode 17: Letter Combinations of a Phone Number (Cartesian Product)
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent. Return the answer in any order.

Constraints:
- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9'].

Complexity:
- Time: O(4^N * N) where N is the length of digits. C-accelerated Cartesian product
  generation via itertools.product.
- Space: O(1) auxiliary space beyond the output list.
"""

import itertools
from typing import List

KEYPAD_MAPPING = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations(digits: str) -> List[str]:
    """
    Generate letter combinations using C-accelerated Cartesian product.

    Key Invariants & Mechanics:
    1. Base Case: If `digits` is empty, return `[]`.
    2. Character Pools: Map each digit to its candidate letter string.
    3. C-Speed Iteration: `itertools.product(*pools)` generates tuples of characters
       directly in C with zero Python frame allocations.
    4. Reconstitution: `''.join(combo)` converts character tuples to strings.
    """
    if not digits:
        return []

    pools = [KEYPAD_MAPPING[d] for d in digits]
    return ["".join(combo) for combo in itertools.product(*pools)]


class Solution:
    """LeetCode submission interface wrapper."""

    def letter_combinations(self, digits: str) -> List[str]:
        return letter_combinations(digits)
