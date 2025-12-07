import heapq
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        #  keep the largest k elements
        heap = []

        for x in nums:
            heapq.heappush(heap, x)

            if len(heap) > k:
                heapq.heappop(heap)

        return heap[0]
