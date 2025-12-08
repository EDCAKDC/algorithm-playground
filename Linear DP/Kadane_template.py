from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        dp[i] = max subarray sum ending at index i
        dp[i] = max(nums[i], dp[i-1] + nums[i])

        Time:  O(n)
        Space: O(1)
        """

        cur_sum = nums[0]
        max_sum = nums[0]

        for num in nums[1:]:
            cur_sum = max(num, cur_sum + num)
            max_sum = max(max_sum, cur_sum)

        return max_sum
