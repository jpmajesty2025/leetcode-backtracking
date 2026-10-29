"""
LeetCode 46: Permutations (In-Place Swapping Backtracking)
https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

Complexity:
- Time: O(N * N!) where N is the length of nums. There are N! leaves in the recursion
  tree, each requiring an O(N) copy into the result list. Internal node state transitions
  consist of O(1) pairwise element swaps.
- Space: O(N) auxiliary recursion stack space. Requires zero boolean/visited arrays
  or auxiliary candidate buffers (O(1) auxiliary heap space beyond output).
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations using in-place swap backtracking.

    Key Invariants & Mechanics:
    1. The array is conceptually divided into two zones at index `start`:
       - `arr[0:start]`: Elements fixed for the current branch of the recursion tree.
       - `arr[start:n]`: Unused candidate elements available for position `start`.
    2. Swapping `arr[start]` with `arr[i]` (for i in [start, n-1]) chooses the next element.
    3. Symmetrical backtracking swap restores array integrity upon returning up the call tree.
    4. To guarantee referential transparency for caller code, a working copy of `nums` is used.
    """
    if not nums:
        return [[]]

    result: List[List[int]] = []
    arr = list(nums)
    n = len(arr)

    def backtrack(start: int) -> None:
        if start == n:
            result.append(arr[:])
            return

        for i in range(start, n):
            arr[start], arr[i] = arr[i], arr[start]
            backtrack(start + 1)
            arr[start], arr[i] = arr[i], arr[start]

    backtrack(0)
    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def permute(self, nums: List[int]) -> List[List[int]]:
        return permute(nums)
