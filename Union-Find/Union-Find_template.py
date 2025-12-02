class UnionFind:
    def __init__(self, n):
        # parent[i] = i means i is the root of its own set
        self.parent = list(range(n))
        # rank is used for union by rank (approx tree height)
        self.rank = [0] * n
        # optional: track component count
        self.count = n

    def find(self, x):
        # Path compression: flatten the tree
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # Find roots
        rx, ry = self.find(x), self.find(y)

        # Already in the same set
        if rx == ry:
            return False

        # Union by rank: attach smaller tree under larger tree
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

        # Merged two components
        self.count -= 1
        return True
