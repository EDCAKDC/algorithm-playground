from typing import List
from collections import defaultdict


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        email_to_id = {}
        email_to_name = {}
        id_counter = 0
        # Assign an id to each unique email and record its name
        for acc in accounts:
            name = acc[0]
            for email in acc[1:]:
                if email not in email_to_id:
                    email_to_id[email] = id_counter
                    id_counter += 1
                    email_to_name[email] = name
        uf = UnionFind(id_counter)
        # Union emails that appear in the same account
        for acc in accounts:
            first_email = acc[1]
            first_id = email_to_id[first_email]
            for email in acc[2:]:
                uf.union(first_id, email_to_id[email])
        # Group emails by their root
        root_to_emails = defaultdict(list)
        for email, idx in email_to_id.items():
            root = uf.find(idx)
            root_to_emails[root].append(email)
        res = []
        for emails in root_to_emails.values():
            emails.sort()
            name = email_to_name[emails[0]]
            res.append([name] + emails)

        return res
