class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)

        if abs(target) > total or (total + target) % 2 != 0:
            return 0
        
        p = (total + target) // 2

        dp = [0] * (p + 1)

        dp[0] = 1

        for num in nums:
            for s in range(p, num - 1, -1):
                dp[s] += dp[s-num]

        return dp[p]