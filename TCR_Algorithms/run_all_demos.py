from collections import defaultdict

from TCR_clonal_family import build_clonal_families_union_find


def hash_clonotype_collapse(cdr3_list):
    """
    Simple hash-based exact clonotype collapse on CDR3 strings.
    """
    groups = defaultdict(list)
    for s in cdr3_list:
        groups[s].append(s)
    return list(groups.values())


if __name__ == "__main__":
    cdr3_demo = [
        "CASSLGQNTIYF",
        "CASSLGQNTIHF",  # 1 aa different
        "CASSLGQNTIYV",  # 1 aa different
        "CASSPPPPPPYF",  # unrelated
        "CASSPPPPPPHF",  # 1 aa different from above
    ]

    print("=== Hash-based exact clonotypes ===")
    exact_groups = hash_clonotype_collapse(cdr3_demo)
    for g in exact_groups:
        print(g)

    print("\n=== Union-Find-based clonal families (edit distance <= 1) ===")
    uf_groups = build_clonal_families_union_find(cdr3_demo)
    for g in uf_groups:
        print(g)
