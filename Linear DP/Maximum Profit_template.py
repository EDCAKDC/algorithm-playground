from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        dp[i] = max money robbed up to house i
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])

        Time:  O(n)
        Space: O(1)
        """

        prev2 = 0  # dp[i-2]
        prev1 = 0  # dp[i-1]

        for num in nums:
            cur = max(prev1, prev2 + num)
            prev2 = prev1
            prev1 = cur

        return prev1
