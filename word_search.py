"""
LeetCode 79: Word Search
https://leetcode.com/problems/word-search/

Given an m x n grid of characters board and a string word, return true if word exists
in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent
cells are horizontally or vertically neighboring. The same letter cell may not be
used more than once.

Constraints:
- m == board.length
- n = board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters.

Complexity:
- Time: O(M * N * 3^L) where M, N are board dimensions and L is word length.
  For each starting cell, the first step has 4 directions, and subsequent steps have
  at most 3 directions (since we cannot immediately revisit the parent cell).
- Space: O(L) auxiliary space for the recursion call stack. Using in-place board
  mutation (`#` marking) completely eliminates hash-set allocation overhead.
"""

from typing import List


def exist(board: List[List[str]], word: str) -> bool:
    """
    Determine if `word` exists in `board` using in-place backtrack marking.

    Key Invariants & Mechanics:
    1. Symmetrical In-Place Mutation:
       Instead of allocating a hash set to track visited cells, temporarily mutate
       `board[r][c]` to a sentinel character (e.g. `'#'`) upon entry, and restore its
       original value upon backtracking. This reduces auxiliary space from O(M*N) to O(1)
       beyond the recursion stack.
    2. Boundary & Character Pruning:
       A branch terminates immediately if indices are out of bounds or if `board[r][c] != word[i]`.
    3. Short-Circuit Evaluation:
       The 4 directional recursive calls are chained via logical `or`, terminating the search
       the microsecond a valid path to `i == len(word)` is discovered.
    """
    if not board or not board[0] or not word:
        return False

    m, n = len(board), len(board[0])
    word_len = len(word)

    if word_len > m * n:
        return False

    def dfs(r: int, c: int, i: int) -> bool:
        if i == word_len:
            return True

        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[i]:
            return False

        # Mark cell as visited in-place
        temp = board[r][c]
        board[r][c] = "#"

        # Explore horizontally and vertically adjacent cells
        found = (
            dfs(r + 1, c, i + 1)
            or dfs(r - 1, c, i + 1)
            or dfs(r, c + 1, i + 1)
            or dfs(r, c - 1, i + 1)
        )

        # Restore original character
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
