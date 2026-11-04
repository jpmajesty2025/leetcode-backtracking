"""
LeetCode 2305: Fair Distribution of Cookies
https://leetcode.com/problems/fair-distribution-of-cookies/

You are given an integer array cookies, where cookies[i] denotes the number of cookies
in the ith bag. You are also given an integer k that denotes the number of children
to distribute all the bags of cookies to. All the cookies in the same bag must go to
the same child and cannot be split up.

The unfairness of a distribution is defined as the maximum total cookies obtained by
a single child in the distribution.

Return the minimum unfairness of all distributions.

Constraints:
- 2 <= cookies.length <= 8
- 2 <= k <= cookies.length
- 1 <= cookies[i] <= 10^5

Complexity:
- Time: O(k^N) worst-case upper bound, where N is cookies.length and k is the number
  of children.
  With descending sort, symmetry breaking for empty children, and branch-and-bound
  pruning, the effective search tree shrinks from k^N to a tiny fraction of states.
- Space: O(N + k) auxiliary space for the recursion call stack and child allocation buckets.
"""

from typing import List


def distribute_cookies(cookies: List[int], k: int) -> int:
    """
    Find the minimum unfairness using branch-and-bound DFS with symmetry breaking.

    Key Invariants & Mechanics:
    1. Descending Sort: Distribute the largest cookie bags first. Placing large items
       early forces child totals to rise quickly, triggering bound pruning early in the tree.
    2. Symmetry Breaking (Crucial!):
       Initially, all k children are identical with sum 0. If assigning a bag to an empty
       child and recursing fails or finishes, trying another empty child would produce an
       isomorphic, identical subtree.
       `if child_sums[i] == 0: break` prunes (k - 1)! symmetrical permutations.
    3. Branch-and-Bound Pruning:
       - If `current_max >= min_unfairness`, abort this branch.
       - If `child_sums[i] + bag >= min_unfairness`, skip assigning to child `i`.
    4. Base Cases:
       - If `k == len(cookies)`: Each child receives exactly one bag; return `max(cookies)`.
       - If `k == 1`: One child receives all bags; return `sum(cookies)`.
    """
    if not cookies or k <= 0:
        return 0

    n = len(cookies)
    if k == n:
        return max(cookies)
    if k == 1:
        return sum(cookies)

    # Sort descending so large bags trigger bound pruning at shallow depths
    sorted_cookies = sorted(cookies, reverse=True)
    child_sums = [0] * k
    min_unfairness = float("inf")

    def dfs(idx: int, current_max: int) -> None:
        nonlocal min_unfairness

        # Pruning 1: Current branch already equals or exceeds best known answer
        if current_max >= min_unfairness:
            return

        # Base case: all bags have been distributed
        if idx == n:
            min_unfairness = min(min_unfairness, current_max)
            return

        bag = sorted_cookies[idx]

        for i in range(k):
            # Pruning 2: If giving bag to child i exceeds best known unfairness, skip
            if child_sums[i] + bag >= min_unfairness:
                continue

            child_sums[i] += bag
            dfs(idx + 1, max(current_max, child_sums[i]))
            child_sums[i] -= bag

            # Pruning 3 (Symmetry Breaking):
            # If child i had 0 cookies before receiving this bag (so it is 0 again now),
            # all subsequent children with 0 cookies are identical. Break immediately!
            if child_sums[i] == 0:
                break

    dfs(0, 0)
    return int(min_unfairness)


class Solution:
    """LeetCode submission interface wrapper."""

    def distributeCookies(self, cookies: List[int], k: int) -> int:
        return distribute_cookies(cookies, k)
