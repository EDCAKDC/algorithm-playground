import heapq
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        # Each element in the heap is a tuple: (frequency, number)
        heap = []

        for num, count in freq.items():
            # Push the current (frequency, number) pair into the heap
            heapq.heappush(heap, (count, num))

            if len(heap) > k:
                heapq.heappop(heap)

        return [num for (count, num) in heap]
