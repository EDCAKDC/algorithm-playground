class Solution:
    def climbStairs(self, n: int) -> int:
        """
        dp[i] = number of ways to reach step i
        dp[i] = dp[i-1] + dp[i-2]

        Time:  O(n)
        Space: O(1)
        """

        if n <= 2:
            return n

        prev2 = 1   # dp[1]
        prev1 = 2   # dp[2]

        for _ in range(3, n + 1):
            cur = prev1 + prev2
            prev2 = prev1
            prev1 = cur

        return prev1
