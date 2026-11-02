from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import numbers_with_same_consecutive_diffs as standard_module
import numbers_with_same_consecutive_diffs_bfs as bfs_module
import numbers_with_same_consecutive_diffs_dp as dp_module

MODULES = [
    standard_module,
    bfs_module,
    dp_module,
]

IMPLS = [m.nums_same_consec_diff for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    n, k = 3, 7
    result = impl(n, k)
    expected = [181, 292, 707, 818, 929]
    assert len(result) == 5
    assert set(result) == set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    n, k = 2, 1
    result = impl(n, k)
    expected = [
        10, 12, 21, 23, 32, 34, 43, 45, 54, 56, 65, 67, 76, 78, 87, 89, 98
    ]
    assert len(result) == 17
    assert set(result) == set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_zero_duplicate_guard(impl):
    # When k == 0, consecutive digits must be identical
    # For n = 3, k = 0 -> 111, 222, ..., 999
    n, k = 3, 0
    result = impl(n, k)
    expected = [111, 222, 333, 444, 555, 666, 777, 888, 999]
    assert len(result) == 9
    assert set(result) == set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_n_equals_one(impl):
    result = impl(1, 0)
    assert set(result) == set(range(10))


@pytest.mark.parametrize("impl", IMPLS)
def test_n_equals_two_k_equals_zero(impl):
    result = impl(2, 0)
    expected = [11, 22, 33, 44, 55, 66, 77, 88, 99]
    assert len(result) == 9
    assert set(result) == set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_n_zero_or_negative(impl):
    assert impl(0, 5) == []
    assert impl(-2, 3) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_maximum_constraint_n9_k1(impl):
    n, k = 9, 1
    result = impl(n, k)
    # Check that each integer has exactly 9 digits and consecutive diff is 1
    for num in result:
        s = str(num)
        assert len(s) == 9
        for i in range(len(s) - 1):
            assert abs(int(s[i + 1]) - int(s[i])) == 1
    # No duplicate integers
    assert len(set(result)) == len(result)


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.numsSameConsecDiff(3, 7)
    assert set(res) == {181, 292, 707, 818, 929}


def _independent_diff_oracle(n: int, k: int) -> List[int]:
    """Independent oracle generating numbers by recursive string building."""
    if n <= 0:
        return []
    if n == 1:
        return list(range(10))
    res = []

    def dfs(curr_s):
        if len(curr_s) == n:
            res.append(int(curr_s))
            return
        last_d = int(curr_s[-1])
        # Candidate 1
        d1 = last_d + k
        if d1 < 10:
            dfs(curr_s + str(d1))
        # Candidate 2 (guard k != 0)
        if k != 0:
            d2 = last_d - k
            if d2 >= 0:
                dfs(curr_s + str(d2))

    for first_d in range(1, 10):
        dfs(str(first_d))
    return res


@pytest.mark.parametrize("impl", IMPLS)
@given(
    n=st.integers(min_value=2, max_value=6),
    k=st.integers(min_value=0, max_value=9),
)
@settings(max_examples=35)
def test_hypothesis_independent_oracle(impl, n, k):
    result = impl(n, k)
    oracle = _independent_diff_oracle(n, k)

    # 1. Exact count agreement
    assert len(result) == len(oracle)

    # 2. Every number has exactly n digits and no leading zeros
    for num in result:
        s = str(num)
        assert len(s) == n
        assert s[0] != "0"
        for i in range(len(s) - 1):
            assert abs(int(s[i + 1]) - int(s[i])) == k

    # 3. All generated numbers are distinct
    assert len(set(result)) == len(result)

    # 4. Exact set agreement with oracle
    assert set(result) == set(oracle)
