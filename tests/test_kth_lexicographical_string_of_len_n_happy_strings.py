import itertools
import pytest
from hypothesis import given, settings, strategies as st

import kth_lexicographical_string_of_len_n_happy_strings as backtracking_module
import kth_lexicographical_string_of_len_n_happy_strings_math as math_module
import kth_lexicographical_string_of_len_n_happy_strings_iterative as iterative_module

MODULES = [
    backtracking_module,
    math_module,
    iterative_module,
]

IMPLS = [m.get_happy_string for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    # n = 1, k = 3 -> "c"
    assert impl(1, 3) == "c"


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    # n = 1, k = 4 -> "" (only 3 happy strings of len 1: "a", "b", "c")
    assert impl(1, 4) == ""


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_3(impl):
    # n = 3, k = 9 -> "cab"
    assert impl(3, 9) == "cab"


@pytest.mark.parametrize("impl", IMPLS)
def test_single_character_strings(impl):
    assert impl(1, 1) == "a"
    assert impl(1, 2) == "b"
    assert impl(1, 3) == "c"
    assert impl(1, 4) == ""


@pytest.mark.parametrize("impl", IMPLS)
def test_all_happy_strings_n_equals_two(impl):
    expected_n2 = ["ab", "ac", "ba", "bc", "ca", "cb"]
    for idx, expected_str in enumerate(expected_n2, start=1):
        assert impl(2, idx) == expected_str
    assert impl(2, 7) == ""


@pytest.mark.parametrize("impl", IMPLS)
def test_max_capacity_boundary_n_equals_three(impl):
    # Total = 3 * 2^(3-1) = 12
    assert impl(3, 12) == "cbc"
    assert impl(3, 13) == ""


@pytest.mark.parametrize("impl", IMPLS)
def test_invalid_and_boundary_inputs(impl):
    assert impl(0, 1) == ""
    assert impl(-2, 1) == ""
    assert impl(3, 0) == ""
    assert impl(3, -5) == ""
    assert impl(3, 1000) == ""


@pytest.mark.parametrize("impl", IMPLS)
def test_upper_constraint_n10_k100(impl):
    res = impl(10, 100)
    assert len(res) == 10
    assert all(res[i] != res[i + 1] for i in range(len(res) - 1))
    assert set(res).issubset({"a", "b", "c"})


@pytest.mark.parametrize("impl", IMPLS)
def test_upper_capacity_n10(impl):
    # 3 * 2^9 = 1536
    last_valid = impl(10, 1536)
    assert len(last_valid) == 10
    assert impl(10, 1537) == ""


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    assert sol.getHappyString(1, 3) == "c"
    assert sol.getHappyString(3, 9) == "cab"
    assert sol.getHappyString(1, 4) == ""


def _independent_happy_string_oracle(n: int, k: int) -> str:
    """Independent oracle generating all 3^n strings via Cartesian product and filtering."""
    if n <= 0 or k <= 0:
        return ""
    all_happy = []
    for candidate in itertools.product("abc", repeat=n):
        s = "".join(candidate)
        if all(s[i] != s[i + 1] for i in range(len(s) - 1)):
            all_happy.append(s)
    all_happy.sort()
    return all_happy[k - 1] if 1 <= k <= len(all_happy) else ""


@pytest.mark.parametrize("impl", IMPLS)
@given(
    n=st.integers(min_value=1, max_value=6),
    k=st.integers(min_value=1, max_value=250),
)
@settings(max_examples=40)
def test_hypothesis_independent_oracle(impl, n, k):
    result = impl(n, k)
    oracle = _independent_happy_string_oracle(n, k)

    # 1. Exact agreement with the Cartesian product oracle
    assert result == oracle

    # 2. Structural validity invariants
    max_count = 3 * (1 << (n - 1))
    if k > max_count:
        assert result == ""
    else:
        assert len(result) == n
        assert set(result).issubset({"a", "b", "c"})
        assert all(result[i] != result[i + 1] for i in range(n - 1))
