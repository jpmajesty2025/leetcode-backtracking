from collections import Counter
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import combination_sum as standard_module
import combination_sum_dp as dp_module
import combination_sum_binary as binary_module

MODULES = [
    standard_module,
    dp_module,
    binary_module,
]

IMPLS = [m.combination_sum for m in MODULES]


def _normalize(combos: List[List[int]]):
    """Normalize combinations into a set of sorted tuples for order-agnostic comparison."""
    return set(tuple(sorted(c)) for c in combos)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    candidates = [2, 3, 6, 7]
    target = 7
    result = impl(candidates, target)
    expected = [[2, 2, 3], [7]]
    assert len(result) == 2
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    candidates = [2, 3, 5]
    target = 8
    result = impl(candidates, target)
    expected = [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert len(result) == 3
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_3(impl):
    candidates = [2]
    target = 1
    result = impl(candidates, target)
    assert result == []


@pytest.mark.parametrize("impl", IMPLS)
def test_single_element_exact_match(impl):
    candidates = [5]
    target = 5
    result = impl(candidates, target)
    assert result == [[5]]


@pytest.mark.parametrize("impl", IMPLS)
def test_target_cannot_be_formed(impl):
    candidates = [4, 6]
    target = 7
    assert impl(candidates, target) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_target_zero_or_negative(impl):
    candidates = [2, 3]
    assert impl(candidates, 0) == []
    assert impl(candidates, -5) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_input_identity(impl):
    candidates = [8, 3, 5, 2]
    original = list(candidates)
    impl(candidates, 10)
    assert candidates == original, "Implementation must not permanently mutate caller candidate list"


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.combination_sum([2, 3, 5], 8)
    assert _normalize(res) == _normalize([[2, 2, 2, 2], [2, 3, 3], [3, 5]])


def _independent_coin_oracle(candidates: List[int], target: int) -> List[List[int]]:
    """Independent oracle using recursive unbounded combination generator."""
    if target <= 0 or not candidates:
        return []
    res = []
    cands = sorted(candidates)

    def search(idx, rem, path):
        if rem == 0:
            res.append(path[:])
            return
        for i in range(idx, len(cands)):
            if cands[i] > rem:
                break
            search(i, rem - cands[i], path + [cands[i]])

    search(0, target, [])
    return res


@pytest.mark.parametrize("impl", IMPLS)
@given(
    candidates=st.lists(
        st.integers(min_value=2, max_value=10),
        min_size=1,
        max_size=5,
        unique=True,
    ),
    target=st.integers(min_value=1, max_value=20),
)
@settings(max_examples=40)
def test_hypothesis_independent_oracle(impl, candidates, target):
    cand_copy = list(candidates)
    result = impl(candidates, target)
    oracle = _independent_coin_oracle(candidates, target)

    # 1. Non-mutation of input
    assert candidates == cand_copy

    # 2. Every combination sums to target
    for combo in result:
        assert sum(combo) == target
        # Every element belongs to candidates
        assert all(x in candidates for x in combo)

    # 3. All combinations are unique (no duplicate multisets)
    sorted_combos = [tuple(sorted(c)) for c in result]
    assert len(sorted_combos) == len(set(sorted_combos))

    # 4. Exact match with oracle
    assert _normalize(result) == _normalize(oracle)
