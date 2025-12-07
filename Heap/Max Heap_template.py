import heapq

# Create a max heap using negative values
heap = []

heapq.heappush(heap, -x)
largest = -heapq.heappop(heap)
