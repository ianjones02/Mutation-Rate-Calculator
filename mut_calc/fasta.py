"""
FASTA parsing utilities.
"""
from __future__ import annotations
from typing import Dict


def read_fasta(path: str) -> Dict[str, str]:
    """
    Read an aligned FASTA file into a dict of id -> sequence (uppercase).

    Assumes that alignment is already performed (all sequences same length).
    If multiple entries share an ID, later ones overwrite earlier.

    Args:
        path: Path to FASTA file.

    Returns:
        Dict mapping sequence IDs to sequences (no '>' in keys).
    """
    seqs: Dict[str, str] = {}
    current_id: str = ""
    chunks: list[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                # Flush previous
                if current_id:
                    seqs[current_id] = "".join(chunks).upper()
                current_id = line[1:].strip()
                chunks = []
            else:
                chunks.append(line)
        # Final flush
        if current_id:
            seqs[current_id] = "".join(chunks).upper()

    return seqs
