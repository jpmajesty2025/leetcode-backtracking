import itertools
import math
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import combinations as standard_module
import combinations_lexicographical as lexico_module
import combinations_gospers as gospers_module

MODULES = [
    standard_module,
    lexico_module,
    gospers_module,
]

IMPLS = [m.combine for m in MODULES]


def _to_frozenset_set(comb_list: List[List[int]]):
    """Normalize a list of combinations into a set of frozensets for order-agnostic comparison."""
    return set(frozenset(c) for c in comb_list)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    n, k = 4, 2
    result = impl(n, k)
    expected = [
        [1, 2],
        [1, 3],
        [1, 4],
        [2, 3],
        [2, 4],
        [3, 4],
    ]
    assert len(result) == 6
    assert _to_frozenset_set(result) == _to_frozenset_set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    n, k = 1, 1
    result = impl(n, k)
    assert result == [[1]]


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_n(impl):
    n, k = 5, 5
    result = impl(n, k)
    assert result == [[1, 2, 3, 4, 5]]


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_one(impl):
    n, k = 4, 1
    result = impl(n, k)
    expected = [[1], [2], [3], [4]]
    assert len(result) == 4
    assert _to_frozenset_set(result) == _to_frozenset_set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_k_greater_than_n(impl):
    assert impl(3, 4) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_k_zero_or_negative(impl):
    assert impl(5, 0) == []
    assert impl(5, -1) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_asymmetric_k_close_to_n(impl):
    # n=6, k=4 -> C(6, 4) = 15
    n, k = 6, 4
    result = impl(n, k)
    assert len(result) == 15
    oracle = [list(c) for c in itertools.combinations(range(1, n + 1), k)]
    assert _to_frozenset_set(result) == _to_frozenset_set(oracle)


@pytest.mark.parametrize("impl", IMPLS)
def test_large_constraint_n20_k16(impl):
    # C(20, 16) = 4,845 combinations
    n, k = 20, 16
    result = impl(n, k)
    assert len(result) == math.comb(20, 16)
    # Check that each combination has unique elements of length k
    assert all(len(c) == 16 for c in result)
    assert len(set(tuple(c) for c in result)) == 4845


def test_lexicographical_order_guarantee():
    n, k = 5, 3
    result = lexico_module.combine(n, k)
    expected = [list(c) for c in itertools.combinations(range(1, n + 1), k)]
    assert result == expected


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    result = sol.combine(4, 2)
    assert len(result) == 6
    assert _to_frozenset_set(result) == _to_frozenset_set([
        [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]
    ])


@pytest.mark.parametrize("impl", IMPLS)
@given(
    data=st.integers(min_value=1, max_value=8).flatmap(
        lambda n: st.tuples(st.just(n), st.integers(min_value=1, max_value=n))
    )
)
@settings(max_examples=40)
def test_hypothesis_independent_oracle(impl, data):
    n, k = data
    result = impl(n, k)

    # 1. Exact count matching C(n, k)
    expected_count = math.comb(n, k)
    assert len(result) == expected_count

    # 2. Every combination has length k
    assert all(len(comb) == k for comb in result)

    # 3. Elements within each combination are valid (in range 1..n)
    for comb in result:
        assert all(1 <= x <= n for x in comb)
        assert len(set(comb)) == k  # strictly unique items

    # 4. All combinations in result are unique
    assert len(set(tuple(comb) for comb in result)) == expected_count

    # 5. Exact match with itertools.combinations oracle
    oracle = [list(c) for c in itertools.combinations(range(1, n + 1), k)]
    assert _to_frozenset_set(result) == _to_frozenset_set(oracle)
