import itertools
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import combination_sum_iii as standard_module
import combination_sum_iii_bitmask as bitmask_module
import combination_sum_iii_itertools as itertools_module

MODULES = [
    standard_module,
    bitmask_module,
    itertools_module,
]

IMPLS = [m.combination_sum_3 for m in MODULES]


def _normalize(combos: List[List[int]]):
    """Convert combinations into a set of sorted tuples for order-agnostic comparison."""
    return set(tuple(sorted(c)) for c in combos)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    k, n = 3, 7
    result = impl(k, n)
    expected = [[1, 2, 4]]
    assert len(result) == 1
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    k, n = 3, 9
    result = impl(k, n)
    expected = [[1, 2, 6], [1, 3, 5], [2, 3, 4]]
    assert len(result) == 3
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_3(impl):
    k, n = 4, 1
    result = impl(k, n)
    assert result == []


@pytest.mark.parametrize("impl", IMPLS)
def test_all_nine_digits(impl):
    # k = 9, sum of 1..9 = 45
    result = impl(9, 45)
    expected = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
    assert len(result) == 1
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_n_too_large(impl):
    # k = 3, max sum is 7 + 8 + 9 = 24
    assert impl(3, 25) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_n_too_small(impl):
    # k = 3, min sum is 1 + 2 + 3 = 6
    assert impl(3, 5) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_k_zero_or_negative(impl):
    assert impl(0, 10) == []
    assert impl(-1, 5) == []
    assert impl(10, 45) == []


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.combinationSum3(3, 7)
    assert _normalize(res) == _normalize([[1, 2, 4]])


def _independent_oracle(k: int, n: int) -> List[List[int]]:
    """Independent oracle generating combinations using itertools."""
    if k <= 0 or k > 9:
        return []
    return [list(c) for c in itertools.combinations(range(1, 10), k) if sum(c) == n]


@pytest.mark.parametrize("impl", IMPLS)
@given(
    k=st.integers(min_value=1, max_value=9),
    n=st.integers(min_value=1, max_value=50),
)
@settings(max_examples=45)
def test_hypothesis_independent_oracle(impl, k, n):
    result = impl(k, n)
    oracle = _independent_oracle(k, n)

    # 1. Exact count agreement
    assert len(result) == len(oracle)

    # 2. Every combination has length k and sum n
    for combo in result:
        assert len(combo) == k
        assert sum(combo) == n
        assert all(1 <= x <= 9 for x in combo)
        assert len(set(combo)) == k  # distinct digits

    # 3. All combinations are unique
    assert len(set(tuple(sorted(c)) for c in result)) == len(result)

    # 4. Exact set match with oracle
    assert _normalize(result) == _normalize(oracle)
