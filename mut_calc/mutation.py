"""
Mutation calculation utilities.
"""
from __future__ import annotations
from typing import Tuple


def compute_mutation_rate(
    ref_seq: str,
    target_seq: str,
    exclude_gaps: bool = False
) -> Tuple[int, int, float]:
    """
    Compute mutation count, comparable positions, and rate for target vs reference.

    Definitions:
    - Comparable positions:
      - If exclude_gaps is True: positions where both ref and target are not '-'
      - Else: all positions
    - Mutation: a position where target != ref (case-insensitive), within comparable positions

    Args:
        ref_seq: Reference sequence (aligned).
        target_seq: Target sequence (aligned).
        exclude_gaps: Whether to exclude positions where either has '-'.

    Returns:
        (mutations, comparable_positions, mutation_rate)
        where mutation_rate = mutations / comparable_positions if comparable_positions > 0 else 0.0
    """
    if len(ref_seq) != len(target_seq):
        raise ValueError("Aligned sequences must be of equal length")

    mutations = 0
    comparable = 0

    for r, t in zip(ref_seq, target_seq):
        if exclude_gaps and (r == "-" or t == "-"):
            continue
        comparable += 1
        if r != t:
            mutations += 1

    rate = (mutations / comparable) if comparable > 0 else 0.0
    return mutations, comparable, rate
