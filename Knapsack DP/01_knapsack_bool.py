def knapsack_01_bool(nums, target):
    """
    0-1 Knapsack (Boolean Version)
    dp[s] = whether we can form sum s using some elements
    """

    dp = [False] * (target + 1)
    dp[0] = True  # Base case: sum = 0 is always achievable

    for num in nums:
        # Traverse backward to avoid reusing the same number
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True

    return dp[target]
