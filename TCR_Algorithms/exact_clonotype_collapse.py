from collections import defaultdict
from typing import List, Tuple, Dict


def hash_clonotype_collapse(
    cells: List[Tuple[str, str, str, str]]
) -> Dict[Tuple[str, str, str], List[str]]:
    """
    O(n)
    Collapse TCR clonotypes by exact (CDR3, V, J) match.

    Parameters
    ----------
    cells : list of tuples
        Each element is (cell_id, cdr3, v_gene, j_gene)

    Returns
    -------
    groups : dict
        Key   = (cdr3, v_gene, j_gene)
        Value = list of cell_ids belonging to this 

    """

    groups = defaultdict(list)

    for cell_id, cdr3, v, j in cells:
        key = (cdr3, v, j)
        groups[key].append(cell_id)
    return groups


# ---- small demo ----
if __name__ == "__main__":
    cells_demo = [
        ("cell1", "CASSLGQNTIYF", "TRBV7-9", "TRBJ2-3"),
        ("cell2", "CASSLGQNTIYF", "TRBV7-9", "TRBJ2-3"),
        ("cell3", "CASSIRSSYEQYF", "TRBV5-1", "TRBJ1-2"),
        ("cell4", "CASSLGQNTIYF", "TRBV7-9", "TRBJ2-3"),
    ]

    groups = collapse_clonotypes(cells_demo)

    for clonotype, cell_ids in groups.items():
        print("Clonotype:", clonotype, "Cells:", cell_ids)
