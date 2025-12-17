"""
Annotate ATAC/ChIP union peaks with gene features using a GTF file.

Outputs per peak:
- annotation_type: promoter / gene_body / intergenic
- gene: matched gene (promoter/gene_body) or nearest_gene (intergenic)
- distance_to_TSS: signed distance from peak center to gene TSS (bp)

Conventions
-----------
- Half-open intervals: [start, end) (BED-like)
- BED is 0-based half-open
- GTF is 1-based closed in spec; we convert to 0-based half-open:
    gtf_start_0 = start-1
    gtf_end_0   = end
"""

from __future__ import annotations

import argparse
import bisect
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


GenomicInterval = Tuple[str, int, int]  # (chrom, start, end)


@dataclass
class GeneRecord:
    chrom: str
    start: int   # 0-based
    end: int     # 0-based end (half-open)
    strand: str
    gene_id: str
    gene_name: str
    tss: int     # 0-based position (TSS as a single coordinate)


@dataclass
class FeatureInterval:
    chrom: str
    start: int
    end: int
    gene_name: str
    tss: int


def parse_gtf_attributes(attr_str: str) -> Dict[str, str]:
    """
    Parse GTF attributes column: key "value"; key2 "value2";
    Returns dict of attributes.
    """
    attrs: Dict[str, str] = {}
    # split by ';' then parse key-value
    for part in attr_str.strip().split(";"):
        part = part.strip()
        if not part:
            continue
        # typical: key "value"
        if " " not in part:
            continue
        key, val = part.split(" ", 1)
        val = val.strip().strip('"')
        attrs[key] = val
    return attrs


def read_gtf_genes(gtf_path: str) -> List[GeneRecord]:
    """
    Read gene records from GTF. Uses rows where feature == 'gene'.
    Converts coordinates to 0-based half-open.
    """
    genes: List[GeneRecord] = []
    with open(gtf_path, "r") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9:
                continue
            chrom, source, feature, start_s, end_s, score, strand, frame, attrs_s = parts
            if feature != "gene":
                continue

            try:
                start_1 = int(start_s)  # 1-based inclusive
                end_1 = int(end_s)      # 1-based inclusive
            except ValueError:
                continue

            # Convert to 0-based half-open
            start = start_1 - 1
            end = end_1  # inclusive -> half-open end

            attrs = parse_gtf_attributes(attrs_s)
            gene_id = attrs.get("gene_id", "")
            gene_name = attrs.get("gene_name", gene_id) or gene_id

            # define TSS
            if strand == "+":
                tss = start
            else:
                # negative strand TSS at gene end-1 in 0-based coordinates
                # gene end is half-open, last base is end-1
                tss = end - 1

            genes.append(GeneRecord(
                chrom=chrom, start=start, end=end, strand=strand,
                gene_id=gene_id, gene_name=gene_name, tss=tss
            ))
    return genes


def read_bed3(bed_path: str) -> List[GenomicInterval]:
    peaks: List[GenomicInterval] = []
    with open(bed_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("#", "track", "browser")):
                continue
            cols = line.split()
            if len(cols) < 3:
                continue
            chrom = cols[0]
            try:
                start = int(cols[1])
                end = int(cols[2])
            except ValueError:
                continue
            if end <= start:
                continue
            peaks.append((chrom, start, end))
    return peaks


def build_promoters(
    genes: List[GeneRecord],
    upstream: int,
    downstream: int,
) -> List[FeatureInterval]:
    feats: List[FeatureInterval] = []
    for g in genes:
        if g.strand == "+":
            p_start = max(0, g.tss - upstream)
            p_end = g.tss + downstream
        else:
            # for '-' strand, upstream is to the right
            p_start = max(0, g.tss - downstream)
            p_end = g.tss + upstream
        if p_end > p_start:
            feats.append(FeatureInterval(
                g.chrom, p_start, p_end, g.gene_name, g.tss))
    return feats


def group_by_chrom_intervals(intervals: List[FeatureInterval]) -> Dict[str, List[FeatureInterval]]:
    grouped: Dict[str, List[FeatureInterval]] = {}
    for it in intervals:
        grouped.setdefault(it.chrom, []).append(it)
    for chrom in grouped:
        grouped[chrom].sort(key=lambda x: x.start)
    return grouped


def group_by_chrom_peaks(peaks: List[GenomicInterval]) -> Dict[str, List[Tuple[int, int, int]]]:
    """
    Returns chrom -> list of (start,end,peak_index), sorted by start.
    """
    grouped: Dict[str, List[Tuple[int, int, int]]] = {}
    for idx, (chrom, start, end) in enumerate(peaks):
        grouped.setdefault(chrom, []).append((start, end, idx))
    for chrom in grouped:
        grouped[chrom].sort(key=lambda x: x[0])
    return grouped


def intervals_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    return a_start < b_end and b_start < a_end


def assign_best_gene_by_tss_distance(
    peak_center: int,
    candidates: List[FeatureInterval],
) -> Tuple[str, int]:
    """
    Choose candidate gene whose TSS is closest to peak_center.
    Returns (gene_name, signed_distance).
    signed_distance = peak_center - tss (bp)
    """
    best_gene = ""
    best_dist = 10**18
    best_signed = 0
    for c in candidates:
        signed = peak_center - c.tss
        dist = abs(signed)
        if dist < best_dist:
            best_dist = dist
            best_signed = signed
            best_gene = c.gene_name
    return best_gene, best_signed


def annotate_overlaps(
    peaks: List[GenomicInterval],
    feature_grouped: Dict[str, List[FeatureInterval]],
) -> Dict[int, List[FeatureInterval]]:
    """
    For each peak index, collect all overlapping feature intervals.
    Uses two-pointer sweep per chromosome.
    """
    peak_grouped = group_by_chrom_peaks(peaks)
    hits: Dict[int, List[FeatureInterval]] = {}

    for chrom in peak_grouped.keys() & feature_grouped.keys():
        p_list = peak_grouped[chrom]          # (pstart, pend, pidx)
        # FeatureInterval, sorted by start
        f_list = feature_grouped[chrom]

        j = 0
        for pstart, pend, pidx in p_list:
            # advance features that end before peak starts
            while j < len(f_list) and f_list[j].end <= pstart:
                j += 1

            # scan forward from j while feature.start < pend
            k = j
            cand: List[FeatureInterval] = []
            while k < len(f_list) and f_list[k].start < pend:
                if intervals_overlap(pstart, pend, f_list[k].start, f_list[k].end):
                    cand.append(f_list[k])
                k += 1

            if cand:
                hits.setdefault(pidx, []).extend(cand)

    return hits


def build_tss_index(genes: List[GeneRecord]) -> Dict[str, Tuple[List[int], List[str]]]:
    """
    chrom -> (sorted_tss_positions, gene_names aligned)
    """
    per_chrom: Dict[str, List[Tuple[int, str]]] = {}
    for g in genes:
        per_chrom.setdefault(g.chrom, []).append((g.tss, g.gene_name))
    index: Dict[str, Tuple[List[int], List[str]]] = {}
    for chrom, arr in per_chrom.items():
        arr.sort(key=lambda x: x[0])
        tss = [x[0] for x in arr]
        names = [x[1] for x in arr]
        index[chrom] = (tss, names)
    return index


def nearest_tss(
    tss_list: List[int],
    name_list: List[str],
    pos: int,
) -> Tuple[str, int]:
    """
    Given sorted tss_list and aligned name_list, find nearest TSS to pos.
    Returns (gene_name, signed_distance = pos - tss)
    """
    if not tss_list:
        return "", 0
    k = bisect.bisect_left(tss_list, pos)
    best_idx = None
    best_dist = 10**18
    best_signed = 0

    for cand in (k - 1, k):
        if 0 <= cand < len(tss_list):
            signed = pos - tss_list[cand]
            dist = abs(signed)
            if dist < best_dist:
                best_dist = dist
                best_signed = signed
                best_idx = cand

    if best_idx is None:
        return "", 0
    return name_list[best_idx], best_signed


def annotate_peaks(
    peaks: List[GenomicInterval],
    genes: List[GeneRecord],
    promoter_upstream: int = 2000,
    promoter_downstream: int = 200,
) -> List[Dict[str, str]]:
    """
    Main annotation routine.
    """
    promoters = build_promoters(
        genes, upstream=promoter_upstream, downstream=promoter_downstream)
    promoter_grouped = group_by_chrom_intervals(promoters)

    gene_bodies = [FeatureInterval(
        g.chrom, g.start, g.end, g.gene_name, g.tss) for g in genes]
    gene_grouped = group_by_chrom_intervals(gene_bodies)

    promoter_hits = annotate_overlaps(peaks, promoter_grouped)
    gene_hits = annotate_overlaps(peaks, gene_grouped)

    tss_index = build_tss_index(genes)

    out: List[Dict[str, str]] = []
    for idx, (chrom, start, end) in enumerate(peaks):
        center = (start + end) // 2

        annotation = "intergenic"
        gene = ""
        dist = 0

        if idx in promoter_hits:
            annotation = "promoter"
            gene, dist = assign_best_gene_by_tss_distance(
                center, promoter_hits[idx])
        elif idx in gene_hits:
            annotation = "gene_body"
            gene, dist = assign_best_gene_by_tss_distance(
                center, gene_hits[idx])
        else:
            # nearest gene fallback
            if chrom in tss_index:
                tss_list, name_list = tss_index[chrom]
                gene, dist = nearest_tss(tss_list, name_list, center)
            else:
                gene, dist = "", 0

        out.append({
            "peak_id": f"peak_{idx}",
            "chrom": chrom,
            "start": str(start),
            "end": str(end),
            "annotation": annotation,
            "gene": gene,
            "distance_to_TSS": str(dist),
        })
    return out


def write_tsv(path: str, rows: List[Dict[str, str]]) -> None:
    cols = ["peak_id", "chrom", "start", "end",
            "annotation", "gene", "distance_to_TSS"]
    with open(path, "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(r.get(c, "") for c in cols) + "\n")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Annotate union peaks with promoter/gene_body/intergenic using GTF.")
    p.add_argument("--peaks-bed", required=True,
                   help="Union peaks BED3 (chrom start end).")
    p.add_argument("--gtf", required=True,
                   help="Gene annotation GTF (must include feature 'gene').")
    p.add_argument("--promoter-upstream", type=int, default=2000,
                   help="Promoter upstream window (bp).")
    p.add_argument("--promoter-downstream", type=int, default=200,
                   help="Promoter downstream window (bp).")
    p.add_argument("--out-tsv", required=True, help="Output TSV annotation.")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    peaks = read_bed3(args.peaks_bed)
    genes = read_gtf_genes(args.gtf)

    rows = annotate_peaks(
        peaks=peaks,
        genes=genes,
        promoter_upstream=args.promoter_upstream,
        promoter_downstream=args.promoter_downstream,
    )
    write_tsv(args.out_tsv, rows)


if __name__ == "__main__":
    main()
