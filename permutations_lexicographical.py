"""
LeetCode 46: Permutations (Iterative Lexicographical Generation)
https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

Complexity:
- Time: O(N log N + N * N!) = O(N * N!) where N is the length of nums. Initial sort takes
  O(N log N). Generating each successive permutation via Narayana Pandita's algorithm takes
  O(N) amortized time, repeated N! - 1 times.
- Space: O(1) auxiliary space beyond the result list. Operates iteratively without
  recursion call stack frames or dynamic graph visitation data structures.
"""

import math
from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations iteratively in lexicographical order.

    Key Invariants & Mechanics (Narayana Pandita's Next Permutation Algorithm):
    1. Sort a working copy of `nums` to start at the lexicographical minimum.
    2. Total number of permutations is strictly N! for distinct elements.
    3. To advance to the next permutation:
       a. Identify pivot `i`: the largest index such that arr[i] < arr[i + 1].
          If no such pivot exists, the array is in descending order (maximum permutation).
       b. Identify successor `j`: the largest index j > i such that arr[j] > arr[i].
       c. Swap arr[i] and arr[j].
       d. Reverse the suffix arr[i + 1:] in-place to minimize the suffix value.
    4. Eliminates call stack frames entirely, guaranteeing O(1) auxiliary memory.
    """
    if not nums:
        return [[]]

    arr = sorted(nums)
    n = len(arr)
    total_permutations = math.factorial(n)
    result: List[List[int]] = [arr[:]]

    for _ in range(total_permutations - 1):
        # Step 1: Find the rightmost pivot where arr[i] < arr[i + 1]
        i = n - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1

        if i < 0:
            break

        # Step 2: Find the rightmost element greater than arr[i]
        j = n - 1
        while arr[j] <= arr[i]:
            j -= 1

        # Step 3: Swap pivot with successor
        arr[i], arr[j] = arr[j], arr[i]

        # Step 4: Reverse the suffix from index i + 1 to n - 1
        left = i + 1
        right = n - 1
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

        result.append(arr[:])

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def permute(self, nums: List[int]) -> List[List[int]]:
        return permute(nums)
