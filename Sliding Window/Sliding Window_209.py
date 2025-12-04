from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        # Left pointer
        left = 0
        sum = 0
        ans = float('inf')
        # Right pointer
        for right in range(n):
            sum += nums[right]

            while sum >= target:
                cur = right - left + 1
                ans = min(ans, cur)
                sum -= nums[left]
                left += 1
        return 0 if ans == float('inf') else ans
