from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import word_search as standard_module
import word_search_optimized as optimized_module
import word_search_trie as trie_module

MODULES = [
    standard_module,
    optimized_module,
    trie_module,
]

IMPLS = [m.exist for m in MODULES]


@pytest.fixture
def example_board():
    return [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl, example_board):
    board = [list(r) for r in example_board]
    assert impl(board, "ABCCED") is True


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl, example_board):
    board = [list(r) for r in example_board]
    assert impl(board, "SEE") is True


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_3(impl, example_board):
    board = [list(r) for r in example_board]
    assert impl(board, "ABCB") is False


@pytest.mark.parametrize("impl", IMPLS)
def test_single_cell_match(impl):
    board = [["A"]]
    assert impl(board, "A") is True


@pytest.mark.parametrize("impl", IMPLS)
def test_single_cell_mismatch(impl):
    board = [["A"]]
    assert impl(board, "B") is False


@pytest.mark.parametrize("impl", IMPLS)
def test_word_longer_than_board_size(impl):
    board = [["A", "B"], ["C", "D"]]
    assert impl(board, "ABCDE") is False


@pytest.mark.parametrize("impl", IMPLS)
def test_missing_character_not_in_board(impl, example_board):
    board = [list(r) for r in example_board]
    assert impl(board, "ABCCEDZ") is False


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_board_contents(impl, example_board):
    board = [list(r) for r in example_board]
    snapshot = [list(r) for r in example_board]
    impl(board, "ABCCED")
    assert board == snapshot, "Backtracking must restore mutated board cells"


@pytest.mark.parametrize("impl", IMPLS)
def test_adversarial_reversal_asymmetry(impl):
    # Board filled with 'A' except one 'B' at the end
    # Word is 'A'*5 + 'B'
    m, n = 4, 4
    board = [["A"] * n for _ in range(m)]
    board[m - 1][n - 1] = "B"
    word = "A" * 5 + "B"
    assert impl(board, word) is True


@pytest.mark.parametrize("impl", IMPLS)
def test_cannot_reuse_same_cell(impl):
    board = [["A", "A"]]
    assert impl(board, "AAA") is False


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module, example_board):
    sol = module.Solution()
    board = [list(r) for r in example_board]
    assert sol.exist(board, "SEE") is True


def _independent_search_oracle(board: List[List[str]], word: str) -> bool:
    """Independent oracle using set-based visited tracking and simple DFS."""
    m, n = len(board), len(board[0])
    L = len(word)
    if L > m * n:
        return False

    def dfs(r, c, idx, visited):
        if idx == L:
            return True
        if r < 0 or r >= m or c < 0 or c >= n or (r, c) in visited or board[r][c] != word[idx]:
            return False

        visited.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if dfs(r + dr, c + dc, idx + 1, visited):
                visited.remove((r, c))
                return True
        visited.remove((r, c))
        return False

    for r in range(m):
        for c in range(n):
            if board[r][c] == word[0] and dfs(r, c, 0, set()):
                return True
    return False


@pytest.mark.parametrize("impl", IMPLS)
@given(
    board_chars=st.lists(
        st.text(alphabet="ABCDE", min_size=3, max_size=3),
        min_size=3,
        max_size=3,
    ),
    word=st.text(alphabet="ABCDE", min_size=1, max_size=5),
)
@settings(max_examples=40)
def test_hypothesis_independent_oracle(impl, board_chars, word):
    board = [list(row) for row in board_chars]
    board_copy = [list(row) for row in board]

    result = impl(board, word)
    oracle = _independent_search_oracle(board_copy, word)

    # 1. State preservation
    assert board == board_copy

    # 2. Strict agreement with independent oracle
    assert result == oracle
