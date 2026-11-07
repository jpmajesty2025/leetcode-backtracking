import itertools
import re
from typing import List, Set
import pytest
from hypothesis import given, settings, strategies as st

import restore_ip_addresses as backtracking_module
import restore_ip_addresses_iterative as iterative_module
import restore_ip_addresses_dp as dp_module

MODULES = [
    backtracking_module,
    iterative_module,
    dp_module,
]

IMPLS = [m.restore_ip_addresses for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    s = "25525511135"
    expected = {"255.255.11.135", "255.255.111.35"}
    assert set(impl(s)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    s = "0000"
    expected = {"0.0.0.0"}
    assert set(impl(s)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_3(impl):
    s = "101023"
    expected = {
        "1.0.10.23",
        "1.0.102.3",
        "10.1.0.23",
        "10.10.2.3",
        "101.0.2.3",
    }
    assert set(impl(s)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_minimum_valid_ip(impl):
    assert impl("1111") == ["1.1.1.1"]


@pytest.mark.parametrize("impl", IMPLS)
def test_maximum_valid_ip(impl):
    assert impl("255255255255") == ["255.255.255.255"]


@pytest.mark.parametrize("impl", IMPLS)
def test_out_of_bounds_lengths(impl):
    assert impl("") == []
    assert impl("1") == []
    assert impl("12") == []
    assert impl("123") == []
    assert impl("1234567890123") == []  # 13 digits
    assert impl("12345678901234567890") == []  # 20 digits


@pytest.mark.parametrize("impl", IMPLS)
def test_unfeasible_octets(impl):
    assert impl("999999999999") == []  # 999 is invalid octet


@pytest.mark.parametrize("impl", IMPLS)
def test_leading_zeros_handling(impl):
    s = "010010"
    expected = {"0.10.0.10", "0.100.1.0"}
    assert set(impl(s)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_non_digit_inputs(impl):
    assert impl("192.168@1.1") == []
    assert impl("000\n") == []
    assert impl("abcd") == []


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    res = sol.restoreIpAddresses("0000")
    assert res == ["0.0.0.0"]


OCTET_REGEX = re.compile(r"^(0|[1-9][0-9]{0,2})$")


def _independent_ip_oracle(s: str) -> Set[str]:
    """Independent oracle generating all 3-split combinations and validating via regex."""
    n = len(s)
    if not s.isdigit() or n < 4 or n > 12:
        return set()

    valid_ips: Set[str] = set()
    for i, j, k in itertools.combinations(range(1, n), 3):
        parts = [s[:i], s[i:j], s[j:k], s[k:]]
        if all(
            OCTET_REGEX.match(p) and int(p) <= 255
            for p in parts
        ):
            valid_ips.add(".".join(parts))

    return valid_ips


@pytest.mark.parametrize("impl", IMPLS)
@given(
    s=st.text(alphabet="0123456789", min_size=0, max_size=16)
)
@settings(max_examples=40)
def test_hypothesis_independent_oracle(impl, s):
    result = impl(s)
    oracle = _independent_ip_oracle(s)

    # 1. Exact match with independent regex oracle
    assert set(result) == oracle

    # 2. No duplicates in output
    assert len(result) == len(set(result))

    # 3. Structural invariants for all returned IPs
    for ip in result:
        segments = ip.split(".")
        assert len(segments) == 4
        assert "".join(segments) == s
        for seg in segments:
            assert 1 <= len(seg) <= 3
            assert 0 <= int(seg) <= 255
            if len(seg) > 1:
                assert seg[0] != "0"
