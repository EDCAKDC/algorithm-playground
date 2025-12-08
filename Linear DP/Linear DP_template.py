from typing import List


def linear_dp_template(arr: List[int]) -> int:
    """
    Generic Linear DP Template
    dp[i] depends on dp[i-1] and possibly dp[i-2]

    State Definition:
        dp[i] = best result up to index i

    Transition:
        dp[i] = f(dp[i-1], dp[i-2], arr[i])

    Time:  O(n)
    Space: O(n)
    """

    n = len(arr)
    if n == 0:
        return 0
    if n == 1:
        return arr[0]

    dp = [0] * n
    dp[0] = arr[0]
    dp[1] = max(arr[0], arr[1])  # example initialization

    for i in range(2, n):
        dp[i] = max(dp[i-1], dp[i-2] + arr[i])  # generic transition

    return dp[-1]
