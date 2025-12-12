from typing import List, Tuple, Dict

Interval = Tuple[int, int]
GenomicInterval = Tuple[str, int, int]


def intervals_overlap(a: Interval, b: Interval) -> bool:
    """
    Return True if two 1D intervals [a_start, a_end) and [b_start, b_end)
    overlap by at least 1 base.

    Overlap condition for half-open intervals:
        a_start < b_end and b_start < a_end
    """

    a_start, a_end = a
    b_start, b_end = b

    return (a_start < b_end) and (b_start < a_end)


def find_overlaps_1d(
    intervals_a: List[Interval],
    intervals_b: List[Interval],
) -> List[Tuple[int, int]]:
    """
    Find all overlaps between two sorted lists of 1D intervals (no chromosome).

    Parameters
    ----------
    intervals_a : list of (start, end)
    intervals_b : list of (start, end)

    Returns
    -------
    overlaps : list of (i, j)
        Each pair (i, j) means intervals_a[i] overlaps intervals_b[j].

    Notes
    - Time complexity: O(len(A) + len(B)).
    """
    a = list(intervals_a)
    b = list(intervals_b)

    a.sort(key=lambda x: x[0])
    b.sort(key=lambda x: x[0])

    i = 0
    j = 0
    result = []
    while i < len(a) and j < len(b):
        a_int = a[i]
        b_int = b[j]

        if intervals_overlap(a_int, b_int):
            result.append((i, j))

        # Move the pointer with the smaller end coordinate
        if a_int[1] <= b_int[1]:
            i += 1
        else:
            j += 1

    return result

#  Genomic interval operations


def group_by_chrom(intervals: List[GenomicInterval]) -> Dict[str, List[Interval]]:
    """
    Group genomic intervals by chromosome.

    Parameters
    ----------
    intervals : list of (chrom, start, end)

    Returns
    -------
    grouped : dict
        Key   = chrom
        Value = list of (start, end), sorted by start.
    """
    grouped: Dict[str, List[Interval]] = {}

    for chrom, start, end in intervals:
        if chrom not in grouped:
            grouped[chrom] = []
        grouped[chrom].append((start, end))

    # Sort each chromosome's intervals by start
    for chrom in grouped:
        grouped[chrom].sort(key=lambda x: x[0])

    return grouped


def find_overlaps_genomic(
    intervals_a: List[GenomicInterval],
    intervals_b: List[GenomicInterval],
) -> List[Tuple[int, int]]:
    """
    Find overlaps between two genomic interval lists, with chromosomes.

    Parameters
    ----------
    intervals_a : list of (chrom, start, end)
        e.g. ATAC peaks.
    intervals_b : list of (chrom, start, end)
        e.g. gene promoters, enhancers, SNP regions.

    Returns
    -------
    overlaps : list of (i, j)
        indices (i, j) refer to original intervals_a[i], intervals_b[j].

    Notes
    -----
    - We only compare intervals on the same chromosome.
    - Inside each chromosome, we do a two-pointer sweep in O(na + nb).
    - Overall complexity: O(N log N) from sorting + linear sweep per chromosome.
    """
    # Pre-group by chromosome, but we also need to remember original indices
    # So we build per-chrom lists with (start, end, original_index).
    grouped_a: Dict[str, List[Tuple[int, int, int]]] = {}
    grouped_b: Dict[str, List[Tuple[int, int, int]]] = {}

    for idx, (chrom, start, end) in enumerate(intervals_a):
        grouped_a.setdefault(chrom, []).append((start, end, idx))

    for idx, (chrom, start, end) in enumerate(intervals_b):
        grouped_b.setdefault(chrom, []).append((start, end, idx))

    # Sort by start within each chromosome
    for chrom in grouped_a:
        grouped_a[chrom].sort(key=lambda x: x[0])
    for chrom in grouped_b:
        grouped_b[chrom].sort(key=lambda x: x[0])

    overlaps: List[Tuple[int, int]] = []

    # For chromosomes that appear in both sets
    for chrom in grouped_a.keys() & grouped_b.keys():
        list_a = grouped_a[chrom]
        list_b = grouped_b[chrom]

        i = 0
        j = 0

        while i < len(list_a) and j < len(list_b):
            a_start, a_end, a_idx = list_a[i]
            b_start, b_end, b_idx = list_b[j]

            # Check overlap
            if (a_start < b_end) and (b_start < a_end):
                overlaps.append((a_idx, b_idx))

            # Move the pointer with smaller end
            if a_end <= b_end:
                i += 1
            else:
                j += 1

    return overlaps

# -------------
#  Small demo
# -------------


if __name__ == "__main__":
    # Example 1: simple 1D intervals (no chromosome)
    print("=== 1D interval overlap demo ===")
    peaks_1d = [(100, 180), (150, 220), (300, 330), (320, 350)]
    genes_1d = [(160, 200), (310, 360)]

    overlaps_1d = find_overlaps_1d(peaks_1d, genes_1d)
    for i, j in overlaps_1d:
        print(f"peak {peaks_1d[i]} overlaps region {genes_1d[j]}")

    # Example 2: genomic intervals with chromosome
    print("\n=== Genomic interval overlap demo ===")
    peaks = [
        ("chr1", 100, 180),
        ("chr1", 150, 220),
        ("chr1", 300, 330),
        ("chr2", 50, 100),
    ]

    promoters = [
        ("chr1", 160, 200),  # overlaps chr1 peaks [100,180] & [150,220]
        ("chr1", 310, 360),  # overlaps chr1 peak [300,330]
        ("chr2", 10, 60),    # overlaps chr2 peak [50,100]
    ]

    overlaps_gen = find_overlaps_genomic(peaks, promoters)
    for i, j in overlaps_gen:
        print(
            f"peak {i}: {peaks[i]} overlaps promoter {j}: {promoters[j]}"
        )
