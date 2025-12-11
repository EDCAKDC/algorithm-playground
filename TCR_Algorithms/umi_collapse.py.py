from typing import List


def umi_collapse_hash(umis: List[str]) -> int:

    unique_umis = set()
    for u in umis:
        unique_umis.add(u)
    return len(unique_umis)
