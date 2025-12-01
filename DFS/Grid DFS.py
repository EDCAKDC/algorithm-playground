from typing import List

if not gird:
    return 0
m, n = len(grid), len(grid[0])


def dfs(sr, sc):
    if sr < 0 or sr >= m or sc < 0 or sc >= n or grid[sr][sc] != '1':
        return
    # visited
    grid[sr][sc] = '0'

    # Explore all 4 directions
    dfs(sr + 1, sc)
    dfs(sr - 1, sc)
    dfs(sr, sc + 1)
    dfs(sr, sc - 1)
    count = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    return count
