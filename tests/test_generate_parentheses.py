import math
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import generate_parentheses as standard_module
import generate_parentheses_dp as dp_module
import generate_parentheses_bfs as bfs_module

MODULES = [
    standard_module,
    dp_module,
    bfs_module,
]

IMPLS = [m.generate_parenthesis for m in MODULES]


def _catalan(n: int) -> int:
    """Compute the n-th Catalan number C_n = (1 / (n + 1)) * comb(2n, n)."""
    return math.comb(2 * n, n) // (n + 1)


def is_valid_parentheses(s: str) -> bool:
    """Verify that a string has well-formed balanced parentheses."""
    balance = 0
    for ch in s:
        if ch == "(":
            balance += 1
        elif ch == ")":
            balance -= 1
        if balance < 0:
            return False
    return balance == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    n = 3
    result = impl(n)
    expected = ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert len(result) == 5
    assert set(result) == set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    n = 1
    assert impl(n) == ["()"]


@pytest.mark.parametrize("impl", IMPLS)
def test_n_equals_two(impl):
    n = 2
    result = impl(n)
    expected = ["(())", "()()"]
    assert len(result) == 2
    assert set(result) == set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_n_zero_or_negative(impl):
    assert impl(0) == []
    assert impl(-1) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_n_equals_four(impl):
    # C_4 = 14
    n = 4
    result = impl(n)
    assert len(result) == 14
    assert len(set(result)) == 14
    assert all(is_valid_parentheses(s) for s in result)


@pytest.mark.parametrize("impl", IMPLS)
def test_maximum_constraint_n_eight(impl):
    # C_8 = 1,430
    n = 8
    result = impl(n)
    assert len(result) == _catalan(8)
    assert len(set(result)) == 1430
    assert all(len(s) == 16 for s in result)
    assert all(is_valid_parentheses(s) for s in result)


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.generateParenthesis(3)
    assert set(res) == {"((()))", "(()())", "(())()", "()(())", "()()()"}


def _independent_parenthesis_oracle(n: int) -> List[str]:
    """Independent oracle generating all valid parentheses via recursive bracket matching."""
    if n <= 0:
        return []
    res = []

    def dfs(s, left, right):
        if len(s) == 2 * n:
            res.append(s)
            return
        if left < n:
            dfs(s + "(", left + 1, right)
        if right < left:
            dfs(s + ")", left, right + 1)

    dfs("", 0, 0)
    return res


@pytest.mark.parametrize("impl", IMPLS)
@given(n=st.integers(min_value=1, max_value=6))
@settings(max_examples=25)
def test_hypothesis_independent_oracle(impl, n):
    result = impl(n)
    oracle = _independent_parenthesis_oracle(n)

    # 1. Exact count matching Catalan number C_n
    expected_count = _catalan(n)
    assert len(result) == expected_count

    # 2. Every string has length 2n and is balanced
    for s in result:
        assert len(s) == 2 * n
        assert is_valid_parentheses(s)

    # 3. All generated combinations are unique
    assert len(set(result)) == expected_count

    # 4. Exact set match with oracle
    assert set(result) == set(oracle)
