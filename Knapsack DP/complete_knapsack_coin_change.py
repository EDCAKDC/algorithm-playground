def coinChange(coins, amount):
    """
    Complete Knapsack - Min Number of Coins
    dp[x] = minimum coins needed to form amount x
    """

    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0

    for coin in coins:  # Each coin can be used unlimited times
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != INF else -1
