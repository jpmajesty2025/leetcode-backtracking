"""
LeetCode 17: Letter Combinations of a Phone Number
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below:
- 2 -> "abc"
- 3 -> "def"
- 4 -> "ghi"
- 5 -> "jkl"
- 6 -> "mno"
- 7 -> "pqrs"
- 8 -> "tuv"
- 9 -> "wxyz"

Constraints:
- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9'].

Complexity:
- Time: O(4^N * N) in the worst case (e.g. digits 7 and 9, each mapping to 4 letters),
  where N is the length of digits. There are at most 4^N combinations, each of length N.
- Space: O(N) auxiliary space for the recursion call stack (excluding the O(4^N * N)
  output list).
"""

from typing import List

# Telephone keypad mapping (digits 2-9)
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
    Generate letter combinations using state-space backtracking recursion.

    Key Invariants & Mechanics:
    1. Base Case: If `digits` is empty, return `[]`.
    2. Path Tracking: `path` carries the string formed so far. Because string lengths
       are small (N <= 4), immutable string concatenation in Python incurs negligible
       overhead while avoiding explicit list join operations at leaf nodes.
    3. State Transition: For each letter mapped to `digits[index]`, recurse on `index + 1`.
    4. Terminal State: When `index == len(digits)`, the full N-letter combination is complete.
    """
    if not digits:
        return []

    result: List[str] = []
    n = len(digits)

    def backtrack(index: int, path: str) -> None:
        if index == n:
            result.append(path)
            return

        for letter in KEYPAD_MAPPING[digits[index]]:
            backtrack(index + 1, path + letter)

    backtrack(0, "")
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def letter_combinations(self, digits: str) -> List[str]:
        return letter_combinations(digits)
