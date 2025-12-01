from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0

        m, n = len(grid), len(grid[0])

        def dfs(sr, sc):
            if sr < 0 or sr >= m or sc < 0 or sc >= n or grid[sr][sc] == 0:
                return 0

            grid[sr][sc] = 0
            area = 1
            # Explore all 4 directions
            area += dfs(sr - 1, sc)
            area += dfs(sr + 1, sc)
            area += dfs(sr, sc - 1)
            area += dfs(sr, sc + 1)
            return area

        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    cur = dfs(i, j)
                    ans = max(ans, cur)

        return ans
