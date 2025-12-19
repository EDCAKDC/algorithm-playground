from collections import deque


def bfs(graph, start):
    visited = set()
    q = deque()

    visited.add(start)
    q.append(start)

    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
    return visited
