from collections import deque

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

visited = set()


def bfs(sr, sc):
    q = deque([sr, sc])
    visited.add((sr, sc))

    while q:
        for _ in range(len(q)):
            r, c = q.popleft()

            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
