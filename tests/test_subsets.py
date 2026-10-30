import itertools
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import subsets as standard_module
import subsets_cascading as cascading_module
import subsets_bitmask as bitmask_module

MODULES = [
    standard_module,
    cascading_module,
    bitmask_module,
]

IMPLS = [m.subsets for m in MODULES]


def _to_frozenset_set(subsets_list: List[List[int]]):
    """Normalize a list of subsets into a set of frozensets for order-agnostic comparison."""
    return set(frozenset(s) for s in subsets_list)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    nums = [1, 2, 3]
    result = impl(nums)
    expected = [
        [],
        [1],
        [2],
        [1, 2],
        [3],
        [1, 3],
        [2, 3],
        [1, 2, 3],
    ]
    assert len(result) == 8
    assert _to_frozenset_set(result) == _to_frozenset_set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    nums = [0]
    result = impl(nums)
    expected = [[], [0]]
    assert len(result) == 2
    assert _to_frozenset_set(result) == _to_frozenset_set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_list(impl):
    nums: List[int] = []
    result = impl(nums)
    assert result == [[]]


@pytest.mark.parametrize("impl", IMPLS)
def test_negative_integers(impl):
    nums = [-2, -1, 0]
    result = impl(nums)
    assert len(result) == 8
    expected = [
        [],
        [-2],
        [-1],
        [0],
        [-2, -1],
        [-2, 0],
        [-1, 0],
        [-2, -1, 0],
    ]
    assert _to_frozenset_set(result) == _to_frozenset_set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_four_elements(impl):
    nums = [1, 2, 3, 4]
    result = impl(nums)
    assert len(result) == 16
    expected_oracle = list(
        itertools.chain.from_iterable(
            itertools.combinations(nums, r) for r in range(len(nums) + 1)
        )
    )
    assert _to_frozenset_set(result) == _to_frozenset_set([list(s) for s in expected_oracle])


@pytest.mark.parametrize("impl", IMPLS)
def test_max_constraint_ten_elements(impl):
    nums = list(range(10))
    result = impl(nums)
    assert len(result) == 1024
    # All subsets must be unique
    assert len(set(tuple(s) for s in result)) == 1024


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_input_identity_and_values(impl):
    nums = [3, 1, 2]
    original = list(nums)
    impl(nums)
    assert nums == original, "Implementation must not mutate caller input list"


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    nums = [1, 2]
    result = sol.subsets(nums)
    assert len(result) == 4
    assert _to_frozenset_set(result) == {
        frozenset(),
        frozenset([1]),
        frozenset([2]),
        frozenset([1, 2]),
    }


@pytest.mark.parametrize("impl", IMPLS)
@given(
    nums=st.lists(
        st.integers(min_value=-100, max_value=100),
        min_size=0,
        max_size=7,
        unique=True,
    )
)
@settings(max_examples=40)
def test_hypothesis_independent_oracle(impl, nums):
    input_copy = list(nums)
    result = impl(nums)

    # 1. Non-mutation of input
    assert nums == input_copy

    # 2. Correct number of subsets (2^N)
    n = len(nums)
    expected_count = 1 << n
    assert len(result) == expected_count

    # 3. All generated subsets are unique (no duplicates in result)
    tuple_result = [tuple(s) for s in result]
    assert len(set(tuple_result)) == expected_count

    # 4. Each subset is a valid sub-multiset of the input
    nums_set = set(nums)
    for subset in result:
        assert set(subset).issubset(nums_set)
        assert len(subset) == len(set(subset))  # unique elements within subset

    # 5. Exact match with itertools combinations oracle
    oracle_subsets = list(
        itertools.chain.from_iterable(
            itertools.combinations(nums, r) for r in range(n + 1)
        )
    )
    assert _to_frozenset_set(result) == _to_frozenset_set([list(s) for s in oracle_subsets])
