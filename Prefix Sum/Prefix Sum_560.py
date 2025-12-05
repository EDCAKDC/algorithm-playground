class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_count = {0: 1}
        prefix_sum = 0
        ans = 0
        for i in nums:
            prefix_sum += i
            # if prefix_sum - k seen before → found valid subarray
            if prefix_sum - k in prefix_count:
                ans += prefix_count[prefix_sum - k]
            # update prefix_count
            prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1
        return ans
