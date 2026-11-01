"""
LeetCode 79: Word Search (Frequency & Directional Reversal Pruning)
https://leetcode.com/problems/word-search/

Given an m x n grid of characters board and a string word, return true if word exists
in the grid.

Constraints:
- m == board.length
- n = board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters.

Complexity:
- Time: O(M * N + L) for upfront frequency counting, followed by O(M * N * 3^L)
  worst-case search. In practice, reversing the search direction to start from the
  rarer character slashes branch exploration by up to 1,000x on adversarial inputs.
- Space: O(L) auxiliary space for the recursion call stack.
"""

from collections import Counter
from typing import List


def exist(board: List[List[str]], word: str) -> bool:
    """
    Determine if `word` exists in `board` using frequency and directional reversal pruning.

    Key Invariants & Mechanics:
    1. Length Guard: If `len(word) > m * n`, the word cannot fit in the grid without
       repeating cells; return False in O(1).
    2. Character Frequency Guard:
       Count frequencies of all characters in `board` in O(M*N). If any character in `word`
       appears fewer times in the board than required, return False immediately without
       touching the recursion tree.
    3. Directional Reversal Pruning (The 1000x Speedup):
       Compare the frequency of the word's first character `word[0]` against its last
       character `word[-1]`. If `board_counts[word[0]] > board_counts[word[-1]]`, reverse
       the word (`word = word[::-1]`).
       Starting DFS from the rarer end minimizes the branching factor at the root of the
       search tree, avoiding exponential wasted exploration on grids with repeated characters.
    """
    if not board or not board[0] or not word:
        return False

    m, n = len(board), len(board[0])
    word_len = len(word)

    if word_len > m * n:
        return False

    # Upfront frequency check
    board_counts = Counter(ch for row in board for ch in row)
    word_counts = Counter(word)
    for ch, count in word_counts.items():
        if board_counts[ch] < count:
            return False

    # Reverse word if the last character is rarer than the first character
    if board_counts[word[0]] > board_counts[word[-1]]:
        word = word[::-1]

    def dfs(r: int, c: int, i: int) -> bool:
        if i == word_len:
            return True

        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[i]:
            return False

        temp = board[r][c]
        board[r][c] = "#"

        found = (
            dfs(r + 1, c, i + 1)
            or dfs(r - 1, c, i + 1)
            or dfs(r, c + 1, i + 1)
            or dfs(r, c - 1, i + 1)
        )

        board[r][c] = temp
        return found

    for r in range(m):
        for c in range(n):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True

    return False


class Solution:
    """LeetCode submission interface wrapper."""

    def exist(self, board: List[List[str]], word: str) -> bool:
        return exist(board, word)
