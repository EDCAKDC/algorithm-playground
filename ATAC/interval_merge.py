def merge_intervals(intervals):
    """
    intervals: list of (start, end)
    return: merged list of intervals
    """

    if not intervals:
        return []
    # sort by start
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for cur_start, cur_end in intervals[1:]:
        last_start, last_end = merged[-1]

        if cur_start <= last_end:
            # overlap → merge
            merged[-1] = (last_start, max(last_end, cur_end))
        else:
            merged.append((cur_start, cur_end))
    return merged
