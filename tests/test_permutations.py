import itertools
import math
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import permutations as standard_module
import permutations_swap as swap_module
import permutations_lexicographical as lexico_module

MODULES = [
    standard_module,
    swap_module,
    lexico_module,
]

IMPLS = [m.permute for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    nums = [1, 2, 3]
    result = impl(nums)
    expected = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert len(result) == 6
    assert set(tuple(p) for p in result) == set(tuple(p) for p in expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    nums = [0, 1]
    result = impl(nums)
    expected = [[0, 1], [1, 0]]
    assert len(result) == 2
    assert set(tuple(p) for p in result) == set(tuple(p) for p in expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_3(impl):
    nums = [1]
    result = impl(nums)
    assert result == [[1]]


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_list(impl):
    nums: List[int] = []
    result = impl(nums)
    assert result == [[]]


@pytest.mark.parametrize("impl", IMPLS)
def test_negative_integers(impl):
    nums = [-1, 0, 1]
    result = impl(nums)
    expected = set(itertools.permutations(nums))
    assert len(result) == 6
    assert set(tuple(p) for p in result) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_larger_input_four_elements(impl):
    nums = [4, 3, 2, 1]
    result = impl(nums)
    expected = set(itertools.permutations(nums))
    assert len(result) == 24
    assert set(tuple(p) for p in result) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_five_elements(impl):
    nums = [10, 20, 30, 40, 50]
    result = impl(nums)
    expected = set(itertools.permutations(nums))
    assert len(result) == 120
    assert set(tuple(p) for p in result) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_preserves_input_identity_and_values(impl):
    nums = [3, 1, 2]
    original = list(nums)
    impl(nums)
    assert nums == original, "Implementation must not permanently mutate the input list"


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    nums = [1, 2]
    result = sol.permute(nums)
    assert set(tuple(p) for p in result) == {(1, 2), (2, 1)}


def test_lexicographical_order_guarantee():
    nums = [3, 1, 2]
    result = lexico_module.permute(nums)
    # The output should be strictly sorted lexicographically
    expected = sorted(itertools.permutations(nums))
    assert [tuple(p) for p in result] == expected


@pytest.mark.parametrize("impl", IMPLS)
@given(
    nums=st.lists(
        st.integers(min_value=-100, max_value=100),
        min_size=0,
        max_size=5,
        unique=True,
    )
)
@settings(max_examples=50)
def test_hypothesis_independent_oracle(impl, nums):
    input_copy = list(nums)
    result = impl(nums)

    # 1. Non-mutation of input
    assert nums == input_copy

    # 2. Correct number of permutations (N!)
    n = len(nums)
    expected_count = math.factorial(n)
    assert len(result) == expected_count

    # 3. All generated permutations are unique
    tuple_result = [tuple(p) for p in result]
    assert len(set(tuple_result)) == expected_count

    # 4. Each permutation contains the exact multiset of original elements
    sorted_input = sorted(nums)
    for perm in result:
        assert sorted(perm) == sorted_input

    # 5. Exact match with itertools.permutations oracle
    expected_set = set(itertools.permutations(nums))
    assert set(tuple_result) == expected_set
