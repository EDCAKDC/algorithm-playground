from collections import deque


def bfs(starts, get_neighbors):

    q = deque()
    visited = set()

    for s in starts:
        q.append(s)
        visited.add(s)
    minutes = 0

    while q:
        size = len(q)
        for _ in range(size):
            node = q.popleft()
            for nei in get_neighbors(node):
                if nei not in visited:
                    visited.add(nei)
                    q.append(nei)
        if q:
            minutes += 1
    return minutes
