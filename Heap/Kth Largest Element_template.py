def findKthLargest(nums, k):
    import heapq

    # Min heap to store the top k largest elements
    heap = []

    for x in nums:
        heapq.heappush(heap, x)

        # Keep the heap size equal to k
        if len(heap) > k:
            heapq.heappop(heap)

    # The root of the heap is the kth largest element
    return heap[0]
