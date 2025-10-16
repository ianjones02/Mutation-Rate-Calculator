#!/usr/bin/env bash
set -euo pipefail

python main.py --input examples/alignment.fasta --reference seq1
python main.py --input examples/alignment.fasta --reference seq1 --exclude-gaps
python main.py --input examples/alignment.fasta --reference seq1 --output results.csv

echo Done
