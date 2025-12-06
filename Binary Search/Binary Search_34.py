class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # Find the first index where nums[i] >= target
        def find_left(nums, target):
            left, right = 0, len(nums) - 1
            ans = len(nums)

            while left <= right:
                mid = (left + right) // 2
                if nums[mid] >= target:
                    ans = mid
                    right = mid - 1
                else:
                    left = mid + 1
            return ans
        # Find the first index where nums[i] > target,
        # then -1 to get right

        def find_right(nums, target):
            left, right = 0, len(nums) - 1
            ans = len(nums)

            while left <= right:
                mid = (left + right) // 2
                if nums[mid] > target:
                    ans = mid
                    right = mid - 1
                else:
                    left = mid + 1
            return ans - 1

        if not nums:
            return [-1, -1]
        L = find_left(nums, target)
        R = find_right(nums, target)
        # L > R → invalid range
        # L == len(nums) → left boundary is out of bounds
        # nums[L] != target → target does not actually exist
        if L > R or L == len(nums) or nums[L] != target:
            return [-1, -1]
        return [L, R]
