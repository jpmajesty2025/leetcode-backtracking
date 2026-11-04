from collections import Counter
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import combination_sum_ii as standard_module
import combination_sum_ii_binary as binary_module
import combination_sum_ii_dp as dp_module

MODULES = [
    standard_module,
    binary_module,
    dp_module,
]

IMPLS = [m.combination_sum_2 for m in MODULES]


def _normalize(combos: List[List[int]]):
    """Normalize combinations into a set of sorted tuples for order-agnostic comparison."""
    return set(tuple(sorted(c)) for c in combos)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    candidates = [10, 1, 2, 7, 6, 1, 5]
    target = 8
    result = impl(candidates, target)
    expected = [
        [1, 1, 6],
        [1, 2, 5],
        [1, 7],
        [2, 6],
    ]
    assert len(result) == 4
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    candidates = [2, 5, 2, 1, 2]
    target = 5
    result = impl(candidates, target)
    expected = [
        [1, 2, 2],
        [5],
    ]
    assert len(result) == 2
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_all_identical_elements(impl):
    candidates = [2, 2, 2, 2]
    target = 4
    result = impl(candidates, target)
    assert _normalize(result) == _normalize([[2, 2]])


@pytest.mark.parametrize("impl", IMPLS)
def test_target_cannot_be_formed(impl):
    candidates = [3, 5, 7]
    target = 4
    assert impl(candidates, target) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_target_zero_or_negative(impl):
    candidates = [1, 2, 3]
    assert impl(candidates, 0) == []
    assert impl(candidates, -4) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_candidates(impl):
    assert impl([], 5) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_input_identity(impl):
    candidates = [10, 1, 2, 7, 6, 1, 5]
    original = list(candidates)
    impl(candidates, 8)
    assert candidates == original, "Implementation must not mutate caller candidate list"


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)
    assert len(res) == 4


def _independent_oracle(candidates: List[int], target: int) -> List[List[int]]:
    """Independent oracle generating unique subsets that sum to target via brute force power set."""
    if target <= 0 or not candidates:
        return []
    import itertools

    valid_combos = set()
    n = len(candidates)
    for r in range(1, n + 1):
        for combo in itertools.combinations(candidates, r):
            if sum(combo) == target:
                valid_combos.add(tuple(sorted(combo)))
    return [list(c) for c in valid_combos]


@pytest.mark.parametrize("impl", IMPLS)
@given(
    candidates=st.lists(
        st.integers(min_value=1, max_value=8),
        min_size=1,
        max_size=6,
    ),
    target=st.integers(min_value=1, max_value=15),
)
@settings(max_examples=35)
def test_hypothesis_independent_oracle(impl, candidates, target):
    cand_copy = list(candidates)
    result = impl(candidates, target)
    oracle = _independent_oracle(candidates, target)

    # 1. Non-mutation of input
    assert candidates == cand_copy

    # 2. Every combination sums to target
    for combo in result:
        assert sum(combo) == target

    # 3. All combinations are unique
    sorted_combos = [tuple(sorted(c)) for c in result]
    assert len(sorted_combos) == len(set(sorted_combos))

    # 4. Each combination is a valid sub-multiset of candidates
    cand_counter = Counter(candidates)
    for combo in result:
        combo_counter = Counter(combo)
        for val, count in combo_counter.items():
            assert count <= cand_counter[val]

    # 5. Exact set match with oracle
    assert _normalize(result) == _normalize(oracle)
