from typing import List

n = len(isConnected)

visited = [False] * n


def dfs(i):
    visited[i] = True
    # Check all possible neighbors j
    for j in range(n):
        if isConnected[i][j] == 1 and not visited[j]:
            dfs[j]


provinces = 0
for i in range(n):
    if not visited[i]:
        provinces += 1
        dfs(i)
return provinces
