import heapq
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []

        for x, y in points:
            dist2 = x * x + y * y
            # push current point with negative distance
            heapq.heappush(heap, (-dist2, x, y))

            if len(heap) > k:
                heapq.heappop(heap)

        return [[x, y] for (_, x, y) in heap]
