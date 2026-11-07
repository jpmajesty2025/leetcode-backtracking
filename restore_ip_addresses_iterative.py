"""
LeetCode 93: Restore IP Addresses (3-Partition Iterative Enumeration)
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
- Time: O(1) deterministic bound. Systematically checks at most 3 * 3 * 3 = 27
  possible 3-dot partition points without recursion or backtracking overhead.
- Space: O(1) auxiliary space beyond the output list.
"""

from typing import List


def restore_ip_addresses(s: str) -> List[str]:
    """
    Restore valid IPv4 addresses by enumerating all 3-dot partition points iteratively.

    Key Invariants & Mechanics:
    1. Fixed Partition Model:
       An IPv4 address has exactly 3 internal dots dividing the string into 4 segments:
       s[0:i], s[i:j], s[j:k], s[k:n].
    2. Strictly Bounded Search Space:
       Because each segment length is in {1, 2, 3}, each partition variable has at most
       3 valid values:
       - 1 <= i <= 3
       - 1 <= j - i <= 3
       - 1 <= k - j <= 3
       - 1 <= n - k <= 3
       This bounds the total candidate triplets (i, j, k) to at most 3^3 = 27 combinations.
    3. Segment Validity:
       A segment is valid iff:
       - 1 <= len(sub) <= 3
       - sub does not have leading zeros (sub == "0" or sub[0] != "0")
       - int(sub) <= 255
    """
    n = len(s)
    if not s.isdigit() or n < 4 or n > 12:
        return []

    result: List[str] = []

    def is_valid(sub: str) -> bool:
        if not sub or (sub[0] == "0" and len(sub) > 1):
            return False
        return int(sub) <= 255

    # 3-dot partition points (i, j, k)
    for i in range(1, min(4, n - 2)):
        s1 = s[:i]
        if not is_valid(s1):
            continue

        for j in range(i + 1, min(i + 4, n - 1)):
            s2 = s[i:j]
            if not is_valid(s2):
                continue

            for k in range(j + 1, min(j + 4, n)):
                s3 = s[j:k]
                s4 = s[k:]
                if len(s4) <= 3 and is_valid(s3) and is_valid(s4):
                    result.append(f"{s1}.{s2}.{s3}.{s4}")

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def restoreIpAddresses(self, s: str) -> List[str]:
        return restore_ip_addresses(s)
