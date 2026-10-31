import itertools
import math
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import lettter_combos_of_a_phone_number as standard_module
import letter_combinations_cascading as cascading_module
import letter_combinations_product as product_module

MODULES = [
    standard_module,
    cascading_module,
    product_module,
]

IMPLS = [m.letter_combinations for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    digits = "23"
    result = impl(digits)
    expected = ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert len(result) == 9
    assert set(result) == set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    digits = ""
    result = impl(digits)
    assert result == []


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_3(impl):
    digits = "2"
    result = impl(digits)
    assert set(result) == {"a", "b", "c"}


@pytest.mark.parametrize("impl", IMPLS)
def test_single_four_letter_digit(impl):
    digits = "7"
    result = impl(digits)
    assert set(result) == {"p", "q", "r", "s"}


@pytest.mark.parametrize("impl", IMPLS)
def test_maximum_constraint_four_digits(impl):
    # Digits "7979" -> 4 * 4 * 4 * 4 = 256 combinations
    digits = "7979"
    result = impl(digits)
    assert len(result) == 256
    assert len(set(result)) == 256
    assert all(len(s) == 4 for s in result)


@pytest.mark.parametrize("impl", IMPLS)
def test_all_digits_from_two_to_nine(impl):
    # Digits "234" -> 3 * 3 * 3 = 27 combinations
    digits = "234"
    result = impl(digits)
    assert len(result) == 27
    assert len(set(result)) == 27
    assert all(len(s) == 3 for s in result)


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    assert set(sol.letter_combinations("2")) == {"a", "b", "c"}


def _independent_keypad_oracle(digits: str) -> List[str]:
    """Independent oracle using Cartesian product of letter lists."""
    if not digits:
        return []
    mapping = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }
    pools = [mapping[d] for d in digits]
    return ["".join(c) for c in itertools.product(*pools)]


@pytest.mark.parametrize("impl", IMPLS)
@given(
    digits=st.text(
        alphabet="23456789",
        min_size=0,
        max_size=4,
    )
)
@settings(max_examples=40)
def test_hypothesis_independent_oracle(impl, digits):
    result = impl(digits)
    oracle = _independent_keypad_oracle(digits)

    # 1. Exact count agreement
    assert len(result) == len(oracle)

    # 2. Every string has length equal to len(digits)
    assert all(len(s) == len(digits) for s in result)

    # 3. All combinations are unique
    assert len(set(result)) == len(result)

    # 4. Exact set match with oracle
    assert set(result) == set(oracle)
