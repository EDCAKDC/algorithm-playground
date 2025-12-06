# --------------------------------------------------------
# Find first and last positions of target in a sorted array.
# If target does not exist, returns [-1, -1].
# --------------------------------------------------------
def find_range(nums, target):
    L = lower_bound(nums, target)
    R = upper_bound(nums, target) - 1

    # Validate: target does not exist
    if L == len(nums) or L > R or nums[L] != target:
        return [-1, -1]

    return [L, R]
