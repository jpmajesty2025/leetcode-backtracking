"""
LeetCode 93: Restore IP Addresses
https://leetcode.com/problems/restore-ip-addresses/

A valid IP address consists of exactly four integers separated by single dots.
Each integer is between 0 and 255 (inclusive) and cannot have leading zeros.

Given a string s containing only digits, return all possible valid IP addresses
that can be formed by inserting dots into s. You are not allowed to reorder or
remove any digits in s. You may return the valid IP addresses in any order.

Constraints:
- 1 <= s.length <= 20
- s consists of digits only.

Complexity:
- Time: O(1) upper bound because the recursion tree depth is strictly 4 and each
  node has at most 3 children (at most 3^4 = 81 total leaf evaluations).
- Space: O(1) auxiliary space (recursion depth at most 4, plus output list).
"""

from typing import List


def restore_ip_addresses(s: str) -> List[str]:
    """
    Restore all valid IPv4 addresses using backtracking with feasibility pruning.

    Key Invariants & Mechanics:
    1. Global Length Guard:
       A valid IPv4 address contains 4 octets of length 1 to 3.
       Therefore, any valid string must satisfy 4 <= len(s) <= 12.
       If out of bounds, return [] in O(1) time without recursing.
    2. Remaining Length Feasibility Bound:
       At any depth, with `k = 4 - len(path)` remaining segments and `rem = n - start`
       remaining characters, we must satisfy `k <= rem <= 3 * k`.
       Any branch violating this envelope is pruned immediately.
    3. Leading Zero Short-Circuit:
       If s[start] == '0', the only valid segment starting at this index is "0".
       Multi-digit segments starting with '0' (e.g. "01", "00") are invalid,
       so branching stops immediately after length 1.
    4. In-Place Path Buffer:
       Uses mutable list `path` with push/pop operations to avoid repeated list
       allocations during recursion.
    """
    n = len(s)
    if not s.isdigit() or n < 4 or n > 12:
        return []

    result: List[str] = []
    path: List[str] = []

    def backtrack(start: int) -> None:
        rem_segments = 4 - len(path)
        rem_chars = n - start

        if rem_segments == 0:
            if rem_chars == 0:
                result.append(".".join(path))
            return

        # Prune branches where remaining characters cannot form rem_segments octets
        if not (rem_segments <= rem_chars <= rem_segments * 3):
            return

        # If current digit is '0', only length 1 is valid (no multi-digit "0x" allowed)
        max_len = 1 if s[start] == "0" else min(3, rem_chars)

        for length in range(1, max_len + 1):
            sub = s[start : start + length]
            if length == 3 and int(sub) > 255:
                continue

            path.append(sub)
            backtrack(start + length)
            path.pop()

    backtrack(0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def restoreIpAddresses(self, s: str) -> List[str]:
        return restore_ip_addresses(s)
