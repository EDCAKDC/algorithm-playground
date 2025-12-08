class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp = [0] * n
        dp[0] = cost[0]
        dp[1] = cost[1]

        for i in range(2, n):
            dp[i] = min(dp[i-1], dp[i-2]) + cost[i]

        return min(dp[n-1], dp[n-2])


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)

        prev2 = cost[0]   # dp[0]
        prev1 = cost[1]   # dp[1]

        # compute dp[i] for i = 2 .. n-1
        for i in range(2, n):
            cur = min(prev1, prev2) + cost[i]  # dp[i]
            prev2 = prev1
            prev1 = cur

        # top can be reached from step n-1 or step n-2
        return min(prev1, prev2)
