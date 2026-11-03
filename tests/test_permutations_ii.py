import itertools
import math
from collections import Counter
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import permutations_ii as standard_module
import permutations_ii_frequency as frequency_module
import permutations_ii_lexicographical as lexico_module

MODULES = [
    standard_module,
    frequency_module,
    lexico_module,
]

IMPLS = [m.permute_unique for m in MODULES]


def _normalize(permutations: List[List[int]]):
    """Normalize permutations into a set of tuples for order-agnostic comparison."""
    return set(tuple(p) for p in permutations)


def _multinomial_coefficient(nums: List[int]) -> int:
    """Calculate the expected number of unique permutations: N! / (n_1! * ... * n_k!)."""
    n = len(nums)
    counts = Counter(nums)
    denom = 1
    for c in counts.values():
        denom *= math.factorial(c)
    return math.factorial(n) // denom


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    nums = [1, 1, 2]
    result = impl(nums)
    expected = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    assert len(result) == 3
    assert _normalize(result) == _normalize(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    nums = [1, 2, 3]
    result = impl(nums)
    assert len(result) == 6
    assert len(set(tuple(p) for p in result)) == 6


@pytest.mark.parametrize("impl", IMPLS)
def test_all_identical_elements(impl):
    nums = [2, 2, 2, 2]
    result = impl(nums)
    assert result == [[2, 2, 2, 2]]


@pytest.mark.parametrize("impl", IMPLS)
def test_single_element(impl):
    assert impl([1]) == [[1]]


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_list(impl):
    assert impl([]) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_negative_numbers(impl):
    nums = [-1, -1, 2]
    result = impl(nums)
    assert len(result) == 3
    assert _normalize(result) == _normalize([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]])


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_input_identity(impl):
    nums = [3, 1, 2, 1]
    original = list(nums)
    impl(nums)
    assert nums == original, "Implementation must not mutate caller input list"


def test_lexicographical_order_guarantee():
    nums = [2, 1, 2]
    result = lexico_module.permute_unique(nums)
    # Expected strictly sorted in lexicographical order:
    expected = [[1, 2, 2], [2, 1, 2], [2, 2, 1]]
    assert result == expected


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.permuteUnique([1, 1, 2])
    assert _normalize(res) == _normalize([[1, 1, 2], [1, 2, 1], [2, 1, 1]])


def _independent_oracle(nums: List[int]) -> List[List[int]]:
    """Independent oracle generating unique permutations via itertools and set deduplication."""
    if not nums:
        return []
    return [list(p) for p in set(itertools.permutations(nums))]


@pytest.mark.parametrize("impl", IMPLS)
@given(
    nums=st.lists(
        st.integers(min_value=-5, max_value=5),
        min_size=1,
        max_size=5,
    )
)
@settings(max_examples=35)
def test_hypothesis_independent_oracle(impl, nums):
    nums_copy = list(nums)
    result = impl(nums)
    oracle = _independent_oracle(nums)

    # 1. Non-mutation of caller list
    assert nums == nums_copy

    # 2. Exact permutation count matching multinomial formula
    expected_count = _multinomial_coefficient(nums)
    assert len(result) == expected_count

    # 3. All generated permutations are unique
    assert len(set(tuple(p) for p in result)) == expected_count

    # 4. Every permutation is a valid multiset rearrangement
    target_counts = Counter(nums)
    for p in result:
        assert len(p) == len(nums)
        assert Counter(p) == target_counts

    # 5. Exact set equivalence with independent oracle
    assert _normalize(result) == _normalize(oracle)
