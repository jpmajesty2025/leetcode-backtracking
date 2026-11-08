from typing import List, Set, Tuple
import pytest
from hypothesis import given, settings, strategies as st

import palindrome_partittioning as backtracking_module
import palindrome_partitioning_dp_table as dp_table_module
import palindrome_partitioning_iterative as iterative_module

MODULES = [
    backtracking_module,
    dp_table_module,
    iterative_module,
]

IMPLS = [m.partition for m in MODULES]


def _to_canonical_set(parts: List[List[str]]) -> Set[Tuple[str, ...]]:
    """Convert partition list to canonical set of tuples for order-independent assertions."""
    return {tuple(p) for p in parts}


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    s = "aab"
    expected = {("a", "a", "b"), ("aa", "b")}
    result = impl(s)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    s = "a"
    expected = {("a",)}
    result = impl(s)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_string(impl):
    assert impl("") == []


@pytest.mark.parametrize("impl", IMPLS)
def test_no_multi_char_palindromes(impl):
    s = "abc"
    expected = {("a", "b", "c")}
    result = impl(s)
    assert _to_canonical_set(result) == expected
    assert len(result) == len(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_all_identical_characters(impl):
    s = "aaaa"
    expected = {
        ("a", "a", "a", "a"),
        ("a", "a", "aa"),
        ("a", "aa", "a"),
        ("a", "aaa"),
        ("aa", "a", "a"),
        ("aa", "aa"),
        ("aaa", "a"),
        ("aaaa",),
    }
    result = impl(s)
    assert _to_canonical_set(result) == expected
    assert len(result) == 8


@pytest.mark.parametrize("impl", IMPLS)
def test_symmetric_palindromes(impl):
    s = "racecar"
    result = impl(s)
    canonical = _to_canonical_set(result)
    assert ("racecar",) in canonical
    assert ("r", "a", "c", "e", "c", "a", "r") in canonical
    assert ("r", "aceca", "r") in canonical
    assert ("r", "a", "cec", "a", "r") in canonical


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.partition("aab")
    assert _to_canonical_set(res) == {("a", "a", "b"), ("aa", "b")}


def _independent_palindrome_oracle(s: str) -> Set[Tuple[str, ...]]:
    """Independent oracle generating all 2^(n-1) binary cut configurations."""
    if not s:
        return set()
    n = len(s)
    valid_partitions: Set[Tuple[str, ...]] = set()

    # There are n - 1 possible cut positions
    total_cuts = 1 << (n - 1)
    for mask in range(total_cuts):
        parts: List[str] = []
        last_cut = 0
        for i in range(n - 1):
            if (mask >> i) & 1:
                parts.append(s[last_cut : i + 1])
                last_cut = i + 1
        parts.append(s[last_cut:])

        if all(part == part[::-1] for part in parts):
            valid_partitions.add(tuple(parts))

    return valid_partitions


@pytest.mark.parametrize("impl", IMPLS)
@given(
    s=st.text(alphabet="abcde", min_size=0, max_size=8)
)
@settings(max_examples=35)
def test_hypothesis_independent_oracle(impl, s):
    result = impl(s)
    canonical_res = _to_canonical_set(result)

    # 1. No duplicates in output
    assert len(result) == len(canonical_res)

    # 2. Structural invariants for all partitions
    for p in result:
        assert "".join(p) == s, "Partition pieces must concatenate to original string"
        assert all(part == part[::-1] for part in p), "Every substring must be a palindrome"

    # 3. Exact agreement with independent binary cut oracle
    oracle_partitions = _independent_palindrome_oracle(s)
    assert canonical_res == oracle_partitions
