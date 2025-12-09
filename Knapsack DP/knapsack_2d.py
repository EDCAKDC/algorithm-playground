def knapsack_2d(weights, values, capacity):
    """
    Classic 2D DP Knapsack
    dp[i][c] = max value using first i items with capacity c
    """

    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]

        for c in range(capacity + 1):
            if c < w:
                dp[i][c] = dp[i - 1][c]
            else:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)

    return dp[n][capacity]
