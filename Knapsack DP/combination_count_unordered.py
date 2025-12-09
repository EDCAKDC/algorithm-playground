def combinationSumCount(coins, target):
    """
    Count number of combinations (order does NOT matter)
    """

    dp = [0] * (target + 1)
    dp[0] = 1

    for coin in coins:
        for s in range(coin, target + 1):
            dp[s] += dp[s - coin]

    return dp[target]
