import itertools
from typing import List, Set, Tuple
import pytest
from hypothesis import given, settings, strategies as st

import non_decreasing_subsequences as backtracking_module
import non_decreasing_subsequences_iterative as iterative_module
import non_decreasing_subsequences_bitmask as bitmask_module

MODULES = [
    backtracking_module,
    iterative_module,
    bitmask_module,
]

IMPLS = [m.find_subsequences for m in MODULES]


def _to_canonical_set(subseqs: List[List[int]]) -> Set[Tuple[int, ...]]:
    """Convert a list of subsequences to a canonical set of tuples for comparison."""
    return {tuple(s) for s in subseqs}


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    nums = [4, 6, 7, 7]
    expected = {
        (4, 6),
        (4, 6, 7),
        (4, 6, 7, 7),
        (4, 7),
        (4, 7, 7),
        (6, 7),
        (6, 7, 7),
        (7, 7),
    }
    result = impl(nums)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected), "Output must contain no duplicate subsequences"


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    nums = [4, 4, 3, 2, 1]
    expected = {(4, 4)}
    result = impl(nums)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_and_single_element(impl):
    assert impl([]) == []
    assert impl([42]) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_strictly_decreasing_array(impl):
    nums = [10, 9, 8, 7, 6, 5]
    assert impl(nums) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_strictly_increasing_array(impl):
    nums = [1, 2, 3]
    expected = {(1, 2), (1, 3), (2, 3), (1, 2, 3)}
    result = impl(nums)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_identical_elements_deduplication(impl):
    nums = [7, 7, 7]
    expected = {(7, 7), (7, 7, 7)}
    result = impl(nums)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_negative_values_and_zeros(impl):
    nums = [-5, 0, -2, 0]
    expected = {(-5, 0), (-5, -2), (-5, -2, 0), (-5, 0, 0), (-2, 0), (0, 0)}
    result = impl(nums)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_input_identity(impl):
    nums = [4, 6, 7, 7]
    original = list(nums)
    impl(nums)
    assert nums == original, "Algorithm must not mutate the caller input list"


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.findSubsequences([4, 4, 3, 2, 1])
    assert _to_canonical_set(res) == {(4, 4)}


def _independent_subsequence_oracle(nums: List[int]) -> Set[Tuple[int, ...]]:
    """Independent oracle generating all index combinations via itertools and filtering."""
    n = len(nums)
    if n < 2:
        return set()

    valid_subseqs: Set[Tuple[int, ...]] = set()
    for r in range(2, n + 1):
        for idx_tuple in itertools.combinations(range(n), r):
            candidate = tuple(nums[i] for i in idx_tuple)
            if all(candidate[j] <= candidate[j + 1] for j in range(len(candidate) - 1)):
                valid_subseqs.add(candidate)

    return valid_subseqs


@pytest.mark.parametrize("impl", IMPLS)
@given(
    nums=st.lists(
        st.integers(min_value=-15, max_value=15),
        min_size=0,
        max_size=8,
    )
)
@settings(max_examples=35)
def test_hypothesis_independent_oracle(impl, nums):
    nums_copy = list(nums)
    result = impl(nums)

    # 1. Non-mutation of caller input
    assert nums == nums_copy

    # 2. Structural invariants for all returned subsequences
    res_set = set()
    for subseq in result:
        assert len(subseq) >= 2, "Each subsequence must have length >= 2"
        assert all(
            subseq[i] <= subseq[i + 1] for i in range(len(subseq) - 1)
        ), "Subsequence elements must be non-decreasing"
        subseq_tuple = tuple(subseq)
        assert subseq_tuple not in res_set, "Duplicate subsequence detected in output"
        res_set.add(subseq_tuple)

    # 3. Exact agreement with the independent combinatorial oracle
    oracle_set = _independent_subsequence_oracle(nums_copy)
    assert res_set == oracle_set
