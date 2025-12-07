import heapq
from collections import Counter


def topKFrequent(nums, k):
    freq = Counter(nums)

    # Min heap storing (frequency, value)
    heap = []

    for num, count in freq.items():
        heapq.heappush(heap, (count, num))

        # If heap size exceeds k, remove the least frequent element
        if len(heap) > k:
            heapq.heappop(heap)

    # Extract only the values from the heap
    return [num for (count, num) in heap]
