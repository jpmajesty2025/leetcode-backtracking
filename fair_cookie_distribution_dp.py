"""
LeetCode 2305: Fair Distribution of Cookies (Bitmask Dynamic Programming - Submask Iteration)
https://leetcode.com/problems/fair-distribution-of-cookies/

Complexity:
- Time: O(k * 3^N) where N is cookies.length.
  There are sum_{i=0}^N C(N, i) * 2^i = 3^N submask transitions per child layer.
  For N=8, 3^8 = 6,561 transitions per child.
- Space: O(2^N) table memory for subset sums and DP states.
"""

from typing import List


def distribute_cookies(cookies: List[int], k: int) -> int:
    """
    Find minimum unfairness using bitmask dynamic programming over submasks.

    Key Invariants & Mechanics:
    1. Subset Sum Precomputation:
       Precompute the cookie sum of all 2^N subsets in O(2^N) time.
    2. DP State:
       `dp[mask]` = minimum unfairness when distributing the cookie subset `mask` among `i` children.
    3. Base Case (1 child):
       `dp[mask] = sum_mask[mask]` (one child gets all cookies in `mask`).
    4. Submask Transition (for child 2 to k):
       For each mask, iterate through its submasks `sub`:
           new_dp[mask] = min_{sub subset mask} (max(dp[mask ^ sub], sum_mask[sub]))
       Using the submask iteration idiom `sub = (sub - 1) & mask` visits all submasks in O(3^N).
    """
    if not cookies or k <= 0:
        return 0

    n = len(cookies)
    if k == n:
        return max(cookies)
    if k == 1:
        return sum(cookies)

    num_subsets = 1 << n

    # Precompute subset sums
    sum_mask = [0] * num_subsets
    for mask in range(num_subsets):
        s = 0
        for j in range(n):
            if (mask >> j) & 1:
                s += cookies[j]
        sum_mask[mask] = s

    # Base case: 1 child gets all bags in the mask
    dp = list(sum_mask)

    # Transition for child 2 to k
    for _ in range(2, k + 1):
        new_dp = [float("inf")] * num_subsets
        for mask in range(num_subsets):
            sub = mask
            # Iterate strictly over non-empty submasks of mask
            while sub > 0:
                cost = max(dp[mask ^ sub], sum_mask[sub])
                if cost < new_dp[mask]:
                    new_dp[mask] = cost
                sub = (sub - 1) & mask

        dp = new_dp

    return int(dp[num_subsets - 1])


class Solution:
    """LeetCode submission interface wrapper."""

    def distributeCookies(self, cookies: List[int], k: int) -> int:
        return distribute_cookies(cookies, k)
