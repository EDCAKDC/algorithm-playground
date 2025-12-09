def permutationSumCount(nums, target):
    """
    Count number of permutations (order DOES matter)
    """

    dp = [0] * (target + 1)
    dp[0] = 1

    for s in range(1, target + 1):
        for num in nums:
            if s >= num:
                dp[s] += dp[s - num]

    return dp[target]
