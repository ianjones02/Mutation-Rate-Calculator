#!/usr/bin/env python3
"""
Main CLI for mutation rate calculation from a FASTA alignment.

- Reads FASTA
- Selects a reference sequence
- Computes per-sequence mutation rate
- Writes CSV to stdout or to a file
"""

from __future__ import annotations
import sys
import argparse
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from mut_calc.fasta import read_fasta
from mut_calc.mutation import compute_mutation_rate


@dataclass
class MutationRecord:
    """Container for a single sequence mutation result."""
    sequence_id: str
    mutations: int
    comparable_positions: int
    mutation_rate: float


class MutationRateApp:
    """
    CLI application to compute mutation rates from a FASTA alignment.

    Responsibilities:
    - Parse CLI arguments
    - Load FASTA
    - Perform computation
    - Output results to stdout or file
    """

    def __init__(self, argv: Optional[List[str]] = None) -> None:
        self.argv = argv

    def build_parser(self) -> argparse.ArgumentParser:
        """Build and return an argparse.ArgumentParser."""
        parser = argparse.ArgumentParser(
            description="Compute per-sequence mutation rate relative to a reference from a FASTA alignment."
        )
        parser.add_argument(
            "--input", "-i", required=True, help="Path to aligned FASTA file."
        )
        parser.add_argument(
            "--reference", "-r", required=True, help="Reference sequence ID (header without '>')."
        )
        parser.add_argument(
            "--exclude-gaps",
            action="store_true",
            help="Exclude positions where either reference or target has a gap ('-') from comparison.",
        )
        parser.add_argument(
            "--output", "-o",
            default=None,
            help="Output CSV file. If omitted, results are printed to stdout.",
        )
        return parser

    def run(self) -> int:
        """Execute the CLI application."""
        parser = self.build_parser()
        args = parser.parse_args(self.argv)

        try:
            seqs = read_fasta(args.input)
        except Exception as e:
            print("Error reading FASTA: " + str(e), file=sys.stderr)
            return 1

        if args.reference not in seqs:
            print("Reference sequence not found: " + args.reference, file=sys.stderr)
            return 2

        ref_seq = seqs[args.reference]
        # Validate alignment (all lengths equal)
        lengths = {len(s) for s in seqs.values()}
        if len(lengths) != 1:
            print("FASTA appears not aligned: sequences have different lengths", file=sys.stderr)
            return 3

        results: List[MutationRecord] = []
        for sid, seq in seqs.items():
            muts, comps, rate = compute_mutation_rate(
                ref_seq=ref_seq,
                target_seq=seq,
                exclude_gaps=args.exclude_gaps
            )
            results.append(
                MutationRecord(
                    sequence_id=sid,
                    mutations=muts,
                    comparable_positions=comps,
                    mutation_rate=rate
                )
            )

        # Output CSV
        header = "sequence_id,mutations,comparable_positions,mutation_rate"
        lines = [header]
        for rec in results:
            line = (
                rec.sequence_id + "," +
                str(rec.mutations) + "," +
                str(rec.comparable_positions) + "," +
                ("{:.6f}".format(rec.mutation_rate))
            )
            lines.append(line)

        csv_out = "\n".join(lines)

        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(csv_out + "\n")
                print("Wrote results to " + args.output, file=sys.stdout)
            except Exception as e:
                print("Error writing output: " + str(e), file=sys.stderr)
                return 4
        else:
            print(csv_out, file=sys.stdout)

        return 0


def main() -> None:
    """Entry point when run as a script."""
    app = MutationRateApp()
    code = app.run()
    raise SystemExit(code)


if __name__ == "__main__":
    main()
