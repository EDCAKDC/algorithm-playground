from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[0])
        merged = []
        count = 0
        for interval in intervals:
            if not merged:
                merged.append(interval)
            else:
                if merged[-1][1] > interval[0]:
                    merged[-1][1] = min(merged[-1][1], interval[1])
                    count += 1
                else:
                    # keep the interval with the smaller end
                    merged.append(interval)
        return count
