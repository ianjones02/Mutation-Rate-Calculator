"""
mut_calc: Utilities for parsing FASTA and computing mutation rates.
"""
from .fasta import read_fasta
from .mutation import compute_mutation_rate

__all__ = ["read_fasta", "compute_mutation_rate"]
