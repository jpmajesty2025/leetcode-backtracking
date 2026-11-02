"""
LeetCode 967: Numbers With Same Consecutive Differences (Dynamic Programming / Digit DP)
https://leetcode.com/problems/numbers-with-same-consecutive-differences/

Given two integers n and k, return an array of all the integers of length n where
the difference between every two consecutive digits is k.

Complexity:
- Time: O(2^(N - 1)) worst case.
- Space: O(2^(N - 1)) table storage for intermediate digit DP states.
"""

from typing import Dict, List


def nums_same_consec_diff(n: int, k: int) -> List[int]:
    """
    Generate all valid n-digit integers using digit dynamic programming.

    Key Invariants & Mechanics (Digit DP):
    1. DP State: `dp[d]` stores all valid numbers of the current length ending in digit `d`.
    2. Base Case: Length 1 integers ending in digits 1..9: `dp[d] = [d]`.
    3. Transition: For length from 2 to n:
       For each digit `d` (0..9):
         Look at preceding digits `prev_d` such that `abs(d - prev_d) == k`.
         Each number in `dp[prev_d]` extends to `num * 10 + d`.
    4. Recombination: Gather all `dp[d]` for d in 0..9.
    """
    if n <= 0:
        return []

    if n == 1:
        return list(range(10))

    # dp[d] = list of valid numbers of current length ending with digit d
    dp: Dict[int, List[int]] = {d: [d] for d in range(1, 10)}

    for _ in range(n - 1):
        new_dp: Dict[int, List[int]] = {d: [] for d in range(10)}
        for d in range(10):
            # Preceding digit can be d - k or d + k
            for prev_d in {d - k, d + k}:
                if 0 <= prev_d < 10 and prev_d in dp:
                    for prev_num in dp[prev_d]:
                        new_dp[d].append(prev_num * 10 + d)
        dp = new_dp

    result: List[int] = []
    for d in range(10):
        result.extend(dp[d])

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def numsSameConsecDiff(self, n: int, k: int) -> List[int]:
        return nums_same_consec_diff(n, k)
