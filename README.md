# Mutation-Rate-Calculator

Compute the mutation rate (fraction of differing positions) for each sequence relative to a user-selected reference sequence in a FASTA alignment.

## Features
- Reads aligned FASTA
- User selects a reference sequence ID
- Computes mutation rate per sequence:
  - rate = mismatches / comparable_positions
  - Gaps can be included or excluded (configurable)
- Outputs CSV to stdout or a file
