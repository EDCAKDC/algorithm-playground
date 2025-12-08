from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        min_price = minimum price seen so far
        profit    = maximum profit so far

        Time:  O(n)
        Space: O(1)
        """

        min_price = float('inf')
        max_profit = 0

        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)

        return max_profit
