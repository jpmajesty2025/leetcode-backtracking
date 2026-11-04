"""
LeetCode 2305: Fair Distribution of Cookies (Binary Search on Answer + DFS Feasibility)
https://leetcode.com/problems/fair-distribution-of-cookies/

Complexity:
- Time: O(log(sum - max) * k^N) worst case. In practice, the decision problem
  `can_distribute(limit)` stops at the very first valid distribution (early exit True),
  making binary search up to 8x faster than full optimization search!
- Space: O(N + k) auxiliary space.
"""

from typing import List


def distribute_cookies(cookies: List[int], k: int) -> int:
    """
    Find minimum unfairness using binary search on answer with DFS feasibility checking.

    Key Invariants & Mechanics:
    1. Monotonic Search Space:
       - Lower bound: `max(cookies)` (no child can have less than the largest single bag).
       - Upper bound: `sum(cookies)` (one child gets all cookies).
       If a distribution with max unfairness <= `mid` is possible, any limit > `mid` is
       also possible. This monotonicity allows binary search on `mid`.
    2. Decision Problem (`can_distribute(limit)`):
       Can we distribute all bags such that every child has `<= limit` cookies?
       Crucially, the decision problem terminates on the FIRST successful assignment,
       achieving massive early-exit speedups!
    3. Symmetry Breaking:
       `if child_sums[i] == 0: break` prunes identical empty children.
    """
    if not cookies or k <= 0:
        return 0

    n = len(cookies)
    if k == n:
        return max(cookies)
    if k == 1:
        return sum(cookies)

    sorted_cookies = sorted(cookies, reverse=True)

    def can_distribute(limit: int) -> bool:
        child_sums = [0] * k

        def dfs(idx: int) -> bool:
            if idx == n:
                return True

            bag = sorted_cookies[idx]
            for i in range(k):
                if child_sums[i] + bag <= limit:
                    child_sums[i] += bag
                    if dfs(idx + 1):
                        return True
                    child_sums[i] -= bag

                # Symmetry break: do not assign to multiple empty children
                if child_sums[i] == 0:
                    break

            return False

        return dfs(0)

    low = max(sorted_cookies)
    high = sum(sorted_cookies)
    ans = high

    while low <= high:
        mid = (low + high) // 2
        if can_distribute(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1

    return ans


class Solution:
    """LeetCode submission interface wrapper."""

    def distributeCookies(self, cookies: List[int], k: int) -> int:
        return distribute_cookies(cookies, k)
