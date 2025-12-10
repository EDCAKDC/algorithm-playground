from collections import defaultdict
from edit_distance import edit_distance_leq_one
from union_find_template import UnionFind


def build_clonal_families_union_find(cdr3_list):
    """
    Build clonal families based on CDR3 edit distance <= 1 using Union-Find.
    """

    n = len(cdr3_list)
    uf = UnionFind(n)
    # Step 1: Build similarity edges by pairwise comparison
    for i in range(n):
        for j in range(i + 1, n):
            if edit_distance_leq_one(cdr3_list[i], cdr3_list[j]):
                uf.union(i, j)

    # Step 2: Collect connected components (clonal families)
    families = defaultdict(list)
    for i, seq in enumerate(cdr3_list):
        root = uf.find(i)
        families[root].append(seq)

    return list(families.values())
