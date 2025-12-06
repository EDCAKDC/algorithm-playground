# --------------------------------------------------------
# Upper Bound
# Returns the first index where nums[i] > target.
# If all elements <= target, returns len(nums).
# --------------------------------------------------------
def upper_bound(nums, target):
    left, right = 0, len(nums) - 1
    ans = len(nums)

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] > target:
            ans = mid
            right = mid - 1
        else:
            left = mid + 1

    return ans
