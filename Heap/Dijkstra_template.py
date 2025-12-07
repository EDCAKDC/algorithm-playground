import heapq


def dijkstra(start, graph):
    # (cost, node)
    heap = [(0, start)]
    visited = set()

    while heap:
        cost, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            heapq.heappush(heap, (new_cost, neighbor))
