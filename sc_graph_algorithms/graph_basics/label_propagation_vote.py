"""
label_propagation_vote.py

Graph-based label propagation with neighbor voting (majority vote).

Compared to BFS "first-come-first-serve" propagation, this version:
- Reduces order-dependence
- Handles conflicts via voting + confidence
- Can keep ambiguous nodes as UNLABELED (tie / low confidence)

Typical usage:
- Start with seed_labels (partial annotations)
- Iteratively assign labels to unlabeled nodes based on labeled neighbors
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, Hashable, Iterable, List, Optional, Tuple


Label = str
Node = Hashable
Graph = Dict[Node, List[Node]]


def _vote_from_neighbors(
    node: Node,
    graph: Graph,
    labels: Dict[Node, Label],
) -> Tuple[Optional[Label], float, int, bool]:
    """
    Compute a vote for `node` based on currently labeled neighbors.

    Returns
    -------
    chosen_label : str or None
        The winning label, or None if no labeled neighbors or tie.
    confidence : float
        top_votes / total_votes. 0.0 if no labeled neighbors.
    total_votes : int
        number of labeled neighbors considered.
    is_tie : bool
        whether the vote is tied among top labels.
    """
    neigh = graph.get(node, [])
    neigh_labels = [labels[v] for v in neigh if v in labels]

    if not neigh_labels:
        return None, 0.0, 0, False

    cnt = Counter(neigh_labels)
    (lab1, v1) = cnt.most_common(1)[0]
    total = sum(cnt.values())

    # check tie: another label has same top votes
    top_labels = [lab for lab, v in cnt.items() if v == v1]
    is_tie = len(top_labels) > 1

    if is_tie:
        return None, v1 / total, total, True

    return lab1, v1 / total, total, False


def label_propagation_vote(
    graph: Graph,
    seed_labels: Dict[Node, Label],
    *,
    max_iters: int = 50,
    min_confidence: float = 0.51,
    min_votes: int = 1,
    freeze_seeds: bool = True,
    return_diagnostics: bool = False,
):
    """
    Iterative label propagation by neighbor majority vote.

    Parameters
    ----------
    graph : dict
        adjacency list: {node: [neighbors...]}
    seed_labels : dict
        initial labeled nodes: {node: label}
    max_iters : int
        maximum number of propagation rounds
    min_confidence : float
        only assign a label if (top_votes / total_votes) >= min_confidence
        - set to 0.51 for strict majority
        - set to 0.34 for "plurality" in 3-way cases (not recommended initially)
    min_votes : int
        require at least this many labeled neighbors to vote
    freeze_seeds : bool
        if True, seed labels will never be overwritten (recommended)
    return_diagnostics : bool
        if True, also return per-node vote info

    Returns
    -------
    labels : dict
        final labels assigned
    diagnostics : dict (optional)
        node -> dict with confidence / votes / tie info (for debugging)
    """
    labels: Dict[Node, Label] = dict(seed_labels)
    seed_set = set(seed_labels.keys())

    diagnostics: Dict[Node, dict] = {}

    for _ in range(max_iters):
        changed = 0
        updates: Dict[Node, Label] = {}

        for node in graph.keys():
            if freeze_seeds and node in seed_set:
                continue

            # already labeled? we could allow refinement, but keep simple for now
            if node in labels:
                continue

            chosen, conf, total_votes, is_tie = _vote_from_neighbors(
                node, graph, labels)

            diagnostics[node] = {
                "chosen": chosen,
                "confidence": conf,
                "total_votes": total_votes,
                "is_tie": is_tie,
            }

            if chosen is None:
                continue
            if total_votes < min_votes:
                continue
            if conf < min_confidence:
                continue

            updates[node] = chosen

        # apply updates (synchronous update -> less order dependence)
        for node, lab in updates.items():
            labels[node] = lab
            changed += 1

        if changed == 0:
            break

    if return_diagnostics:
        return labels, diagnostics
    return labels
