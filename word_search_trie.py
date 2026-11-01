"""
LeetCode 79: Word Search (Prefix-Tree / Trie Engine)
https://leetcode.com/problems/word-search/

Given an m x n grid of characters board and a string word, return true if word exists
in the grid.

Complexity:
- Time: O(M * N * 3^L) worst case.
- Space: O(L) for the Trie node structure and call stack.
"""

from typing import Dict, List, Optional


class TrieNode:
    """Trie node storing children characters and terminal word status."""

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_terminal: bool = False


class Trie:
    """Prefix tree supporting word insertion."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_terminal = True


def exist(board: List[List[str]], word: str) -> bool:
    """
    Determine if `word` exists in `board` using a prefix-tree (Trie) traversal.

    Key Invariants & Mechanics:
    1. Trie Representation: Build a prefix tree from `word`.
    2. Synchronized DFS: Traverse `board` and `Trie` concurrently.
       If the current character does not exist in `node.children`, prune immediately.
    3. Scalability: This engine directly generalizes to LeetCode 212 (Word Search II),
       where multiple words are searched simultaneously in a single board pass.
    """
    if not board or not board[0] or not word:
        return False

    m, n = len(board), len(board[0])
    if len(word) > m * n:
        return False

    trie = Trie()
    trie.insert(word)

    found = False

    def dfs(r: int, c: int, node: TrieNode) -> bool:
        nonlocal found
        ch = board[r][c]
        if ch not in node.children:
            return False

        next_node = node.children[ch]
        if next_node.is_terminal:
            found = True
            return True

        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != "#":
                if dfs(nr, nc, next_node):
                    board[r][c] = ch
                    return True

        board[r][c] = ch
        return False

    for r in range(m):
        for c in range(n):
            if dfs(r, c, trie.root):
                return True

    return False


class Solution:
    """LeetCode submission interface wrapper."""

    def exist(self, board: List[List[str]], word: str) -> bool:
        return exist(board, word)
