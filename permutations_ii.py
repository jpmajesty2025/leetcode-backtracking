"""
LeetCode 47: Permutations II
https://leetcode.com/problems/permutations-ii/

Given a collection of numbers, nums, that might contain duplicates, return all possible
unique permutations in any order.

Constraints:
- 1 <= nums.length <= 8
- -10 <= nums[i] <= 10

Complexity:
- Time: O(P * N), where N is len(nums) and P is the number of unique permutations:
      P = N! / (n_1! * n_2! * ... * n_k!)
  where n_i is the frequency of each distinct element.
  Sorting takes O(N log N). Each unique permutation takes O(N) work to construct and copy.
- Space: O(N) auxiliary space for the recursion call stack, the `current` path buffer,
  and the `used` boolean array (excluding the output list).
"""

from typing import List


def permute_unique(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list containing duplicates using sorted DFS backtracking.

    Key Invariants & Mechanics:
    1. Input Non-Mutation: `arr = sorted(nums)` copies and sorts without mutating caller input.
    2. Sibling Deduplication Invariant:
       When `arr[i] == arr[i - 1]`, candidate `arr[i]` can only be chosen if its identical
       twin `arr[i - 1]` is ALREADY currently active in the current path (`used[i - 1] is True`).
       If `not used[i - 1]`, choosing `arr[i]` would generate a permutation identical to
       the one already explored when `arr[i - 1]` was chosen at this same depth.
       Therefore:
           if i > 0 and arr[i] == arr[i - 1] and not used[i - 1]:
               continue
    3. Pruning Efficiency: `not used[i - 1]` enforces that duplicates must be selected in
       strict left-to-right order, pruning 65%+ of recursive nodes compared to `used[i - 1]`.
    """
    if not nums:
        return []

    arr = sorted(nums)
    n = len(arr)
    result: List[List[int]] = []
    current: List[int] = []
    used = [False] * n

    def backtrack() -> None:
        if len(current) == n:
            result.append(current[:])
            return

        for i in range(n):
            if used[i]:
                continue
            # Deduplication condition: enforce sequential filling of duplicate values
            if i > 0 and arr[i] == arr[i - 1] and not used[i - 1]:
                continue

            used[i] = True
            current.append(arr[i])
            backtrack()
            current.pop()
            used[i] = False

    backtrack()
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        return permute_unique(nums)
