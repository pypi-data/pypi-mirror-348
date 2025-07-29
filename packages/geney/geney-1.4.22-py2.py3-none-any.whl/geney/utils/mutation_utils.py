__all__ = ['MutationalEvent', 'Mutation']

import re
from typing import List, Optional
import pandas as pd
import numpy as np

class Mutation:
    def __init__(self, gene: str, chrom: str, pos: int, ref: str, alt: str):
        self.gene = gene
        self.chrom = chrom
        self.pos = int(pos)
        self.ref = ref
        self.alt = alt
        self.mut_type = self._infer_type()

    def _infer_type(self):
        if self.ref == '-' or self.alt == '-':
            return 'indel'
        elif len(self.ref) == len(self.alt) == 1:
            return 'snp'
        else:
            return 'indel'

    def overlaps_with(self, other: 'Mutation') -> bool:
        ref_len = len(self.ref) if self.ref != '-' else 0
        alt_len = len(self.alt) if self.alt != '-' else 0
        span = max(ref_len, alt_len, 1)
        return not (self.pos + span <= other.pos or other.pos + span <= self.pos)

    def to_dict(self):
        return {
            'gene': self.gene,
            'chrom': self.chrom,
            'pos': self.pos,
            'ref': self.ref,
            'alt': self.alt,
            'type': self.mut_type
        }

    def __repr__(self):
        return f"{self.gene}:{self.chrom}:{self.pos}:{self.ref}:{self.alt}"


class MutationalEvent:
    def __init__(self, mut_id: str):
        self.raw = mut_id
        self.mutations: List[Mutation] = self._parse_mutations(mut_id)
        self.gene = self._verify_same_gene()

    def __len__(self):
        return len(self.mutations)

    def _parse_mutations(self, mut_id: str) -> List[Mutation]:
        parts = re.split(r'[|,]', mut_id)
        mutations = []
        for part in parts:
            match = re.match(r'^([^:]+):([^:]+):(\d+):([ACGTN\-]+):([ACGTN\-]+)$', part)
            if not match:
                raise ValueError(f"Invalid format for mutation: {part}")
            mutations.append(Mutation(*match.groups()))
        return mutations

    def _verify_same_gene(self) -> Optional[str]:
        genes = {m.gene for m in self.mutations}
        if len(genes) != 1:
            raise ValueError(f"Multiple genes found in event: {genes}")
        return genes.pop()

    def compatible(self) -> bool:
        # Check for non-overlapping mutations
        for i, m1 in enumerate(self.mutations):
            for j, m2 in enumerate(self.mutations):
                if i != j and m1.overlaps_with(m2):
                    return False
        return True

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([m.to_dict() for m in self.mutations])

    def __repr__(self):
        muts = ', '.join(f"{m.pos}:{m.ref}>{m.alt}" for m in self.mutations)
        return f"MutationalEvent({self.gene} -> [{muts}])"

    @property
    def positions(self):
        return [m.pos for m in self.mutations]

    @property
    def position(self):
        return int(np.mean(self.positions))

    @property
    def types(self):
        return [m.mut_type for m in self.mutations]

    def mutation_args(self):
        """
        Yields (pos, ref, alt) tuples for each mutation, for use with `apply_mutation`.
        """
        return [(m.pos, m.ref, m.alt) for m in self.mutations]

    def __iter__(self):
        return iter(self.mutation_args())
