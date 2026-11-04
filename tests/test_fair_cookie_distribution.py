from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import fair_cookie_distribution as standard_module
import fair_cookie_distribution_binsearch as binsearch_module
import fair_cookie_distribution_dp as dp_module

MODULES = [
    standard_module,
    binsearch_module,
    dp_module,
]

IMPLS = [m.distribute_cookies for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    cookies = [8, 15, 10, 20, 8]
    k = 2
    assert impl(cookies, k) == 31


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    cookies = [6, 1, 3, 2, 2, 4, 1, 2]
    k = 3
    assert impl(cookies, k) == 7


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_n(impl):
    cookies = [4, 9, 2, 7]
    assert impl(cookies, 4) == 9


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_one(impl):
    cookies = [4, 9, 2, 7]
    assert impl(cookies, 1) == 22


@pytest.mark.parametrize("impl", IMPLS)
def test_all_identical_bags(impl):
    cookies = [5, 5, 5, 5]
    assert impl(cookies, 2) == 10


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_input_identity(impl):
    cookies = [8, 15, 10, 20, 8]
    original = list(cookies)
    impl(cookies, 2)
    assert cookies == original, "Implementation must not permanently mutate caller list"


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    assert sol.distributeCookies([8, 15, 10, 20, 8], 2) == 31


def _independent_cookie_oracle(cookies: List[int], k: int) -> int:
    """Independent oracle generating all k^N distributions by brute force recursion."""
    if not cookies or k <= 0:
        return 0
    n = len(cookies)
    child_sums = [0] * k
    best = float("inf")

    def dfs(idx):
        nonlocal best
        if idx == n:
            best = min(best, max(child_sums))
            return
        for i in range(k):
            child_sums[i] += cookies[idx]
            dfs(idx + 1)
            child_sums[i] -= cookies[idx]
            if child_sums[i] == 0:
                break

    dfs(0)
    return best


@pytest.mark.parametrize("impl", IMPLS)
@given(
    cookies=st.lists(
        st.integers(min_value=1, max_value=30),
        min_size=2,
        max_size=6,
    ),
    k_offset=st.integers(min_value=0, max_value=4),
)
@settings(max_examples=35)
def test_hypothesis_independent_oracle(impl, cookies, k_offset):
    # Ensure 2 <= k <= len(cookies)
    k = min(len(cookies), max(2, 2 + k_offset))
    cookies_copy = list(cookies)

    result = impl(cookies, k)
    oracle = _independent_cookie_oracle(cookies_copy, k)

    # 1. Non-mutation of caller list
    assert cookies == cookies_copy

    # 2. Result is within lower and upper theoretical bounds
    assert result >= max(cookies)
    assert result <= sum(cookies)

    # 3. Exact agreement with oracle
    assert result == oracle
