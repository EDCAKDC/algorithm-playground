# --------------------------------------------------------
# Lower Bound
# Returns the first index where nums[i] >= target.
# If target is larger than all elements, returns len(nums).
# --------------------------------------------------------
def lower_bound(nums, target):
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
