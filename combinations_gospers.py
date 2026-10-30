"""
LeetCode 77: Combinations (Gosper's Hack Bit Manipulation)
https://leetcode.com/problems/combinations/

Given two integers n and k, return all possible combinations of k numbers chosen
from the range [1, n]. You may return the answer in any order.

Constraints:
- 1 <= n <= 20
- 1 <= k <= n

Complexity:
- Time: O(C(n, k) * n) where C(n, k) = n! / (k! * (n - k)!). Advancing to the next bitmask
  with Gosper's hack takes O(1) bitwise operations. Extracting the set bits takes O(n)
  operations per combination.
- Space: O(1) auxiliary space beyond the output list. Operates purely through bitwise
  register manipulation with zero call stack frames.
"""

from typing import List


def combine(n: int, k: int) -> List[List[int]]:
    """
    Generate all k-combinations from 1..n using Gosper's Hack.

    Key Invariants & Mechanics (Gosper's Hack, HAKMEM Item 175):
    1. Bitmask Representation: A k-combination corresponds to an integer whose binary
       representation has Hamming weight (popcount) exactly equal to k.
    2. Starting Mask: Smallest integer with k set bits: `(1 << k) - 1`.
    3. Next Mask with same Hamming weight in O(1) bitwise operations:
       - `c = mask & -mask` extracts the lowest set bit.
       - `r = mask + c` adds lowest bit, flipping lowest contiguous block of 1s to 0s
         and setting the bit above them.
       - `mask = (((r ^ mask) >> 2) // c) | r` shifts the remaining bits right to the
         lowest positions and bitwise-ORs with `r`.
    4. Terminates when `mask >= (1 << n)`.
    """
    if k <= 0 or k > n:
        return []

    result: List[List[int]] = []
    mask = (1 << k) - 1
    limit = 1 << n

    while mask < limit:
        # Extract 1-based indices of set bits
        comb = [j + 1 for j in range(n) if (mask >> j) & 1]
        result.append(comb)

        # Gosper's Hack: advance to the next integer with k bits set
        c = mask & -mask
        r = mask + c
        if c == 0:
            break
        mask = (((r ^ mask) >> 2) // c) | r

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def combine(self, n: int, k: int) -> List[List[int]]:
        return combine(n, k)
