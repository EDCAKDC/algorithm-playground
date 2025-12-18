"""
Motif scanner (PWM + sliding window) for ATAC/ChIP genomic sequences.

What this module provides
-------------------------
1) Reverse complement for DNA sequences.
2) Build a PWM in log-likelihood ratio (LLR) form.
3) Slide a window across a sequence and score each k-mer.
4) Scan both strands (+ and -) and report top motif hits.

Notes
-----
- This is a minimal, dependency-free educational / research-ready implementation.
- In real pipelines, sequences come from reference genome FASTA and peaks (BED).
  Here we focus on the core algorithm: sliding window motif scoring.
"""

from typing import Dict, List, Tuple, Optional
import math

# A PWM can be represented as: pwm[pos][base] = probability
PWM = List[Dict[str, float]]

BASES = ("A", "C", "G", "T")
_COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}


# --------------------------
# Basic DNA utility functions
# --------------------------

def reverse_complement(seq: str) -> str:
    """
    Reverse complement of a DNA sequence.
    Unknown bases (e.g., N) are kept as 'N'.
    """
    seq = seq.upper()
    return "".join(_COMP.get(b, "N") for b in reversed(seq))


def is_valid_dna_kmer(kmer: str) -> bool:
    """
    True if kmer contains only A/C/G/T.
    """
    for b in kmer:
        if b not in _COMP:  # A,C,G,T only
            return False
    return True


# --------------------------
# PWM / scoring
# --------------------------

def pwm_to_llr(
    pwm: PWM,
    background: Optional[Dict[str, float]] = None,
    eps: float = 1e-12,
) -> PWM:
    """
    Convert a probability PWM into log-likelihood ratio PWM:
        llr[pos][base] = log2( pwm[pos][base] / background[base] )

    Parameters
    ----------
    pwm : list of dict
        pwm[pos] is dict: {A: pA, C: pC, G: pG, T: pT}
        probabilities should sum to ~1 at each position.
    background : dict or None
        base background frequencies (default uniform 0.25 each).
    eps : float
        small value to avoid log(0).

    Returns
    -------
    llr_pwm : list of dict
        same structure but values are log2 ratios.
    """
    if background is None:
        background = {b: 0.25 for b in BASES}

    llr_pwm: PWM = []
    for pos in range(len(pwm)):
        row = {}
        for b in BASES:
            p = max(pwm[pos].get(b, 0.0), eps)
            bg = max(background.get(b, 0.0), eps)
            row[b] = math.log(p / bg, 2)  # log2
        llr_pwm.append(row)

    return llr_pwm


def score_kmer_llr(kmer: str, llr_pwm: PWM) -> float:
    """
    Score a k-mer using LLR PWM (sum over positions).
    Requires kmer length == len(llr_pwm) and only A/C/G/T.
    """
    score = 0.0
    for i, b in enumerate(kmer):
        score += llr_pwm[i][b]
    return score


# --------------------------
# Sliding window scanning
# --------------------------

def scan_sequence_pwm(
    seq: str,
    llr_pwm: PWM,
    strand: str = "+",
    return_all_scores: bool = True,
) -> List[Tuple[int, float, str]]:
    """
    Scan a sequence with a PWM using a sliding window.

    Parameters
    ----------
    seq : str
        DNA sequence (A/C/G/T/N...)
    llr_pwm : PWM
        LLR PWM of length k
    strand : '+' or '-'
        '+' scans seq as-is.
        '-' scans reverse complement of seq, and reports coordinates on original seq.
    return_all_scores : bool
        If True, return a list of (pos, score, kmer) for every valid window.
        If False, still returns all valid windows; filtering is done by caller.

    Returns
    -------
    hits : list of (pos, score, kmer)
        pos is 0-based start in the original sequence coordinates.
        For strand '-', pos still refers to original coordinate.
    """
    seq = seq.upper()
    k = len(llr_pwm)

    if strand not in ("+", "-"):
        raise ValueError("strand must be '+' or '-'")

    # Prepare scan sequence
    scan_seq = seq if strand == "+" else reverse_complement(seq)
    hits: List[Tuple[int, float, str]] = []

    for i in range(0, len(scan_seq) - k + 1):
        kmer = scan_seq[i:i+k]
        if not is_valid_dna_kmer(kmer):
            continue

        score = score_kmer_llr(kmer, llr_pwm)

        # Convert i back to original coordinates if scanning reverse complement:
        # If scan_seq is RC(seq), then a window starting at i in RC corresponds to:
        # original start = len(seq) - (i + k)
        if strand == "-":
            orig_i = len(seq) - (i + k)
        else:
            orig_i = i

        hits.append((orig_i, score, kmer))

    return hits


def scan_both_strands(
    seq: str,
    llr_pwm: PWM,
) -> List[Tuple[int, float, str, str]]:
    """
    Scan both strands and return combined hits:
        (pos, score, kmer, strand)
    """
    hits_plus = [(pos, score, kmer, "+") for pos, score,
                 kmer in scan_sequence_pwm(seq, llr_pwm, strand="+")]
    hits_minus = [(pos, score, kmer, "-") for pos, score,
                  kmer in scan_sequence_pwm(seq, llr_pwm, strand="-")]
    return hits_plus + hits_minus


def top_hits(
    hits: List[Tuple[int, float, str, str]],
    top_n: int = 10,
    min_score: Optional[float] = None,
) -> List[Tuple[int, float, str, str]]:
    """
    Take top motif hits by score, optionally filter by min_score.
    """
    if min_score is not None:
        hits = [h for h in hits if h[1] >= min_score]
    hits.sort(key=lambda x: x[1], reverse=True)
    return hits[:top_n]


# --------------------------
# Demo
# --------------------------
if __name__ == "__main__":
    # A tiny toy PWM (length 6) for demonstration.
    # This motif roughly prefers: A C G T A A
    pwm_demo: PWM = [
        {"A": 0.85, "C": 0.05, "G": 0.05, "T": 0.05},
        {"A": 0.05, "C": 0.85, "G": 0.05, "T": 0.05},
        {"A": 0.05, "C": 0.05, "G": 0.85, "T": 0.05},
        {"A": 0.05, "C": 0.05, "G": 0.05, "T": 0.85},
        {"A": 0.85, "C": 0.05, "G": 0.05, "T": 0.05},
        {"A": 0.85, "C": 0.05, "G": 0.05, "T": 0.05},
    ]

    llr = pwm_to_llr(pwm_demo)

    seq_demo = "TTTACGTAAGGGACGTAATTTCCCNACGTAAGT"
    print("Sequence:", seq_demo)
    print("Motif length:", len(llr))

    hits = scan_both_strands(seq_demo, llr)
    best = top_hits(hits, top_n=10)

    print("\n=== Top hits (pos, score, kmer, strand) ===")
    for pos, score, kmer, strand in best:
        print(f"{pos:3d}\t{score:8.3f}\t{kmer}\t{strand}")
