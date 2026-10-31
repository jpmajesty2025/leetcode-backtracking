"""
LeetCode 17: Letter Combinations of a Phone Number (Iterative Cascading / BFS)
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent. Return the answer in any order.

Constraints:
- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9'].

Complexity:
- Time: O(4^N * N) where N is the length of digits. Builds combinations iteratively
  layer-by-layer across digits.
- Space: O(1) auxiliary space beyond the output list. Operates iteratively without
  call stack frames or recursive overhead.
"""

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
    Generate letter combinations using iterative cascading (layer-by-layer BFS expansion).

    Key Invariants & Mechanics:
    1. Base Case: If `digits` is empty, return `[]`.
    2. Dynamic Accumulation: Start with `result = [""]`.
    3. Cartesian Expansion: For each digit, produce all pairings of existing prefixes
       with the letters mapped to that digit via list comprehension.
    4. Pythonic Optimization: Leverages C-level comprehension loops in CPython, outperforming
       recursive bytecode dispatch.
    """
    if not digits:
        return []

    result: List[str] = [""]
    for digit in digits:
        result = [prefix + letter for prefix in result for letter in KEYPAD_MAPPING[digit]]

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def letter_combinations(self, digits: str) -> List[str]:
        return letter_combinations(digits)
