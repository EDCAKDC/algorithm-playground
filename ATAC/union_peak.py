# union_peak.py
"""
Union peak construction for ATAC/ChIP peaks across multiple samples.

Goal
----
Given multiple peak lists (per sample), build a unified non-overlapping "union peak set".

This is the standard step for:
- building peaks × samples (or peaks × cells) count matrix
- downstream clustering / DA peaks
- consistent peak indexing across conditions

Conventions
-----------
- Genomic intervals are treated as half-open: [start, end)
- A peak is a tuple: (chrom, start, end)
"""

from typing import Dict, List, Tuple, Optional
from collections import defaultdict

GenomicInterval = Tuple[str, int, int]


def merge_intervals_1d(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Classic interval merge for 1D intervals [start, end).
    """
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for s, e in intervals[1:]:
        last_s, last_e = merged[-1]
        if s <= last_e:  # overlap or touch
            merged[-1] = (last_s, max(last_e, e))
        else:
            merged.append((s, e))
    return merged


def union_peaks(
    peaks_by_sample: Dict[str, List[GenomicInterval]],
    return_membership: bool = False,
) -> Tuple[List[GenomicInterval], Optional[Dict[GenomicInterval, List[str]]]]:
    """
    Build union peaks across multiple samples.

    Parameters
    ----------
    peaks_by_sample : dict
        {sample_id: [(chrom, start, end), ...], ...}
    return_membership : bool
        If True, also return a mapping:
            union_peak -> list of samples that contributed (overlapped) it

    Returns
    -------
    union_list : list of (chrom, start, end)
        A unified non-overlapping peak set across all samples.
    membership : dict or None
        Only if return_membership=True.
        Maps each union peak to samples whose original peaks overlap it.
    """
    # 1) Collect all peaks per chromosome (across all samples)
    chrom_to_all_intervals: Dict[str,
                                 List[Tuple[int, int]]] = defaultdict(list)
    chrom_to_sample_intervals: Dict[str, Dict[str, List[Tuple[int, int]]]] = defaultdict(
        lambda: defaultdict(list))

    for sample, peaks in peaks_by_sample.items():
        for chrom, start, end in peaks:
            chrom_to_all_intervals[chrom].append((start, end))
            if return_membership:
                chrom_to_sample_intervals[chrom][sample].append((start, end))

    # 2) Merge per chromosome to create union peaks
    union_list: List[GenomicInterval] = []
    for chrom in sorted(chrom_to_all_intervals.keys()):
        merged_1d = merge_intervals_1d(chrom_to_all_intervals[chrom])
        union_list.extend([(chrom, s, e) for s, e in merged_1d])

    if not return_membership:
        return union_list, None

    # 3) (Optional) Build membership: union_peak -> which samples overlap it
    #    We'll do a two-pointer sweep per chromosome per sample (efficient & clean).
    membership: Dict[GenomicInterval, List[str]] = {p: [] for p in union_list}

    # Build union per chrom for easy scanning
    union_by_chrom: Dict[str, List[Tuple[int, int,
                                         GenomicInterval]]] = defaultdict(list)
    for chrom, s, e in union_list:
        union_by_chrom[chrom].append((s, e, (chrom, s, e)))
    for chrom in union_by_chrom:
        union_by_chrom[chrom].sort(key=lambda x: x[0])

    def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        # [a0,a1) overlaps [b0,b1) if a0 < b1 and b0 < a1
        return a[0] < b[1] and b[0] < a[1]

    for chrom, sample_map in chrom_to_sample_intervals.items():
        union_chr = union_by_chrom.get(chrom, [])
        if not union_chr:
            continue

        for sample, ints in sample_map.items():
            ints = sorted(ints, key=lambda x: x[0])
            i = 0  # pointer for sample intervals
            j = 0  # pointer for union intervals

            while i < len(ints) and j < len(union_chr):
                s_int = ints[i]
                u_s, u_e, u_key = union_chr[j]

                if overlaps(s_int, (u_s, u_e)):
                    membership[u_key].append(sample)

                # move pointer with smaller end
                if s_int[1] <= u_e:
                    i += 1
                else:
                    j += 1

    # Ensure unique sample list per union peak
    for k in membership:
        membership[k] = sorted(set(membership[k]))

    return union_list, membership


# ----------------
# Small demo
# ----------------
if __name__ == "__main__":
    peaks_by_sample_demo = {
        "sampleA": [
            ("chr1", 100, 180),
            ("chr1", 300, 330),
            ("chr2", 50, 90),
        ],
        "sampleB": [
            ("chr1", 150, 220),
            ("chr1", 320, 350),
            ("chr2", 80, 120),
        ],
        "sampleC": [
            ("chr1", 210, 260),
            ("chr2", 10, 40),
        ],
    }

    print("=== Union peaks (no membership) ===")
    union_list, _ = union_peaks(peaks_by_sample_demo, return_membership=False)
    for p in union_list:
        print(p)

    print("\n=== Union peaks + membership ===")
    union_list, membership = union_peaks(
        peaks_by_sample_demo, return_membership=True)
    for p in union_list:
        print(p, " <- ", membership[p])
