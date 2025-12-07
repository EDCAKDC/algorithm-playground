import heapq

# Create an empty min heap
heap = []

# Push element
heapq.heappush(heap, x)

# Pop the smallest element
smallest = heapq.heappop(heap)

# Peek the smallest element (top of heap)
top = heap[0]
