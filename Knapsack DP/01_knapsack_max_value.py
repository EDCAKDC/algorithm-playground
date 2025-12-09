def knapsack_01_value(weights, values, capacity):
    """
    0-1 Knapsack (Max Value Version)
    Each item can be used at most once
    """

    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        w = weights[i]
        v = values[i]

        # Backward traversal to ensure each item is used only once
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)

    return dp[capacity]
