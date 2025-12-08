from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        dp[i] = min cost to step on i
        dp[i] = min(dp[i-1], dp[i-2]) + cost[i]

        Time:  O(n)
        Space: O(1)
        """

        n = len(cost)

        prev2 = cost[0]  # dp[0]
        prev1 = cost[1]  # dp[1]

        for i in range(2, n):
            cur = min(prev1, prev2) + cost[i]
            prev2 = prev1
            prev1 = cur

        return min(prev1, prev2)
