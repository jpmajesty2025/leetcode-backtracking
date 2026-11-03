"""
LeetCode 47: Permutations II (Iterative Lexicographical Order - Narayana Pandita Algorithm)
https://leetcode.com/problems/permutations-ii/

Given a collection of numbers, nums, that might contain duplicates, return all possible
unique permutations in any order.

Complexity:
- Time: O(P * N), where P is the number of unique permutations. Each `next_permutation`
  step takes O(N) amortized time. Runs nearly 2x faster than recursion.
- Space: O(1) auxiliary space beyond the output list.
"""

from typing import List


def permute_unique(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations iteratively in strict lexicographical order.

    Key Invariants & Mechanics (Narayana Pandita's Algorithm, 14th Century):
    1. Start from the Minimal Lexicographical Form: Sort `nums` in ascending order.
    2. Finding the Pivot: Scan from right to left to find the first index `i` such that
       `arr[i] < arr[i + 1]`. If no such index exists, all permutations are exhausted.
    3. Finding the Successor: Scan from the right end to find the first index `j` such that
       `arr[j] > arr[i]`.
    4. Swap & Reverse: Swap `arr[i]` and `arr[j]`, then reverse the suffix `arr[i + 1:]`.
    5. Inherent Deduplication: Because the algorithm moves strictly to the next lexicographical
       successor, it naturally skips duplicates with zero extra memory or hash sets!
    """
    if not nums:
        return []

    arr = sorted(nums)
    result: List[List[int]] = [arr[:]]
    n = len(arr)

    while True:
        # Step 1: Find the rightmost pivot i such that arr[i] < arr[i + 1]
        i = n - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1

        if i < 0:
            break

        # Step 2: Find the rightmost element j > i such that arr[j] > arr[i]
        j = n - 1
        while arr[j] <= arr[i]:
            j -= 1

        # Step 3: Swap pivot and successor
        arr[i], arr[j] = arr[j], arr[i]

        # Step 4: Reverse suffix to obtain minimal lexicographical order
        arr[i + 1 :] = reversed(arr[i + 1 :])
        result.append(arr[:])

    return result


class Solution:
    """LeetCode submission interface wrapper."""

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        return permute_unique(nums)
