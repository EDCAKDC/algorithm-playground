def count_subarrays_with_sum(nums, k):
    prefix_count = {0: 1}  # prefix sum value
    prefix_sum = 0
    result = 0

    for x in nums:
        prefix_sum += x

        # prefix_sum - previous_prefix = k
        if prefix_sum - k in prefix_count:
            result += prefix_count[prefix_sum - k]

        # store current prefix_sum
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return result
