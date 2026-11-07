"""
LeetCode 93: Restore IP Addresses (Layer-by-Layer Dynamic Programming)
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
- Time: O(1) bounded. Builds valid prefixes layer-by-layer across 4 segment stages,
  with each stage examining at most 3 character transitions per prefix boundary.
- Space: O(1) auxiliary space beyond the output list.
"""

from typing import List


def restore_ip_addresses(s: str) -> List[str]:
    """
    Restore valid IPv4 addresses using bottom-up layer-by-layer dynamic programming.

    Key Invariants & Mechanics:
    1. DP State Formulation:
       Let `dp[seg][end]` be the collection of valid segment segmentations
       covering the prefix `s[:end]` using exactly `seg` segments (1 <= seg <= 4).
    2. Feasibility Bounds:
       At stage `seg`, the valid prefix length `end` must satisfy `seg <= end <= 3 * seg`.
       Any index outside this range cannot possibly complete an IPv4 address.
    3. State Transition:
       To form `seg` segments ending at index `end`:
       Examine trailing segment lengths L in {1, 2, 3}.
       If `sub = s[end - L : end]` is a valid segment, extend every segmentation
       from `dp[seg - 1][end - L]`.
    4. Base & Final Answer:
       Initialize seg = 1 directly from valid prefixes s[:L].
       The final answer is extracted from `dp[4][n]`.
    """
    n = len(s)
    if not s.isdigit() or n < 4 or n > 12:
        return []

    def is_valid(sub: str) -> bool:
        if not sub or (sub[0] == "0" and len(sub) > 1):
            return False
        return int(sub) <= 255

    # dp[end] stores list of valid segmented prefixes for current segment count
    dp: List[List[List[str]]] = [[] for _ in range(n + 1)]

    # Layer 1: valid 1-segment prefixes
    for length in range(1, min(4, n + 1)):
        sub = s[:length]
        if is_valid(sub):
            dp[length].append([sub])

    # Layers 2, 3, 4
    for seg in range(2, 5):
        next_dp: List[List[List[str]]] = [[] for _ in range(n + 1)]
        min_end = seg
        max_end = min(seg * 3, n)

        for end in range(min_end, max_end + 1):
            for length in range(1, min(4, end + 1)):
                start = end - length
                if start < 0 or not dp[start]:
                    continue

                sub = s[start:end]
                if is_valid(sub):
                    for prev_parts in dp[start]:
                        next_dp[end].append(prev_parts + [sub])

        dp = next_dp

    return [".".join(parts) for parts in dp[n]]


class Solution:
    """LeetCode submission interface wrapper."""

    def restoreIpAddresses(self, s: str) -> List[str]:
        return restore_ip_addresses(s)
