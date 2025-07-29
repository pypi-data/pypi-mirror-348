from __future__ import annotations

__all__ = ['SeqMat', 'format_mut_id']


from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional
from collections import defaultdict
import numpy as np
import pandas as pd



def format_mut_id(text):
    import re
    # text = "TP53:17:7579472:G:A"

    pattern = r'^[^:]+:[^:]+:(\d+):([ACGTN\-]+):([ACGTN\-]+)$'
    match = re.match(pattern, text)

    if match:
        position = int(match.group(1))
        ref = match.group(2)
        alt = match.group(3)
        return {'pos': position, 'ref': ref, 'alt': alt}

        # print(f"Position: {position}, Ref: {ref}, Alt: {alt}")
    else:
        print("No match")
        return None


@dataclass(slots=True)
class SeqMat:
    """Represents a genomic sequence matrix used for training."""
    name: str = field(default="Unnamed Sequence")
    version: str = field(default="1.0")
    source: str = field(default="Unknown")
    notes: dict = field(default_factory=dict)

    seq_array: np.ndarray = field(init=False, repr=False)
    insertion_counters: dict = field(default_factory=lambda: defaultdict(int), init=False, repr=False)
    rev: bool = field(default=False, init=False, repr=False)
    predicted_splicing: pd.DataFrame = field(init=False, repr=False)

    def __init__(
            self,
            nucleotides: str,
            index: np.ndarray,
            conservation: Optional[np.ndarray] = None,
            reference_nucleotides: Optional[np.ndarray] = None,
            notes: Optional[dict] = None,
            source: Optional[str] = None,
            rev: Optional[bool] = False,
            name: Optional[str] = 'wild_type',
            version: Optional[str] = 'none'
    ) -> None:
        # Metadata
        self.name = name
        self.version = version
        self.source = source or "Unknown"
        self.notes = notes or {}
        self.rev = rev
        self.predicted_splicing = None

        # Build structured array
        nts = np.array(list(nucleotides), dtype='S1')
        L = len(nts)
        if index.shape[0] != L:
            raise ValueError("Indices length must match sequence length.")
        if conservation is not None and conservation.shape[0] != L:
            raise ValueError("Conservation length must match sequence length.")
        if reference_nucleotides is not None and len(reference_nucleotides) != L:
            raise ValueError("Reference nucleotides length must match sequence length.")

        dtype = np.dtype([
            ('nt', 'S1'),
            ('index', np.float64),
            ('ref', 'S1'),
            ('cons', np.float32),
            ('valid_mask', bool)
        ])
        self.seq_array = np.empty(L, dtype=dtype)
        self.seq_array['nt'] = nts
        self.seq_array['ref'] = nts if reference_nucleotides is None else np.array(reference_nucleotides, dtype='S1')
        self.seq_array['index'] = index
        self.seq_array['cons'] = np.zeros(L, dtype='f4') if conservation is None else conservation
        self.seq_array['valid_mask'] = self.seq_array['nt'] != b'-'

        self.insertion_counters = defaultdict(int)

    @property
    def seq(self) -> str:
        return self.seq_array['nt'][self.seq_array['valid_mask']].tobytes().decode()

    @property
    def index(self) -> np.ndarray:
        return self.seq_array['index'][self.seq_array['valid_mask']]

    @property
    def conservation(self) -> np.ndarray:
        return self.seq_array['cons'][self.seq_array['valid_mask']]

    def clone(self, start: Optional[float] = None, end: Optional[float] = None) -> SeqMat:
        new = SeqMat.__new__(SeqMat)
        new.name = self.name
        new.version = self.version
        new.source = self.source
        new.notes = self.notes.copy()
        new.rev = self.rev
        new.predicted_splicing = None
        new.insertion_counters = defaultdict(int)

        if start is not None and end is not None:
            mask = (self.seq_array['index'] >= start) & (self.seq_array['index'] <= end)
            new.seq_array = self.seq_array[mask].copy()
        else:
            new.seq_array = self.seq_array.copy()

        new.seq_array['valid_mask'] = new.seq_array['nt'] != b'-'
        return new

    def apply_mutations(
            self,
            mutations: Union[Tuple[float, str, str], List[Tuple[float, str, str]]],
            only_snps: bool = False
    ) -> SeqMat:
        """
        Apply one or a batch of mutations (pos, ref, alt) efficiently:
        - Supports a single tuple or a list of tuples
        - Assumes mutations sorted by position for vectorized searchsorted
        """
        # Normalize to list
        if isinstance(mutations, tuple) and len(mutations) == 3:
            mutations = [mutations]
        elif not isinstance(mutations, list):
            raise TypeError("mutations must be a tuple or list of tuples")

        # Left-normalize and bucket
        subs, ins, dels = [], [], []
        for pos, ref, alt in mutations:
            while ref and alt and ref[0] == alt[0]:
                pos += 1
                ref = ref[1:] or '-'
                alt = alt[1:] or '-'
            if ref != '-' and alt != '-':
                subs.append((pos, ref, alt))
            elif ref == '-' and alt != '-' and not only_snps:
                ins.append((pos, alt))
            elif alt == '-' and ref != '-' and not only_snps:
                dels.append((pos, ref))
            else:
                raise ValueError(f"Unsupported mutation {pos}:{ref}:{alt}.")

        # Ensure seq_array indices sorted
        coords = self.seq_array['index']

        # 1) Bulk substitutions
        if subs:
            subs.sort(key=lambda x: x[0])
            positions = np.array([p for p, _, _ in subs], dtype=coords.dtype)
            idxs = np.searchsorted(coords, positions)
            for (pos, ref, alt), idx in zip(subs, idxs):
                length = len(ref)
                if not np.all(self.seq_array['ref'][idx:idx + length] == np.frombuffer(ref.encode(), dtype='S1')):
                    actual = self.seq_array['ref'][idx:idx + length].tobytes().decode()
                    raise ValueError(f"Ref mismatch at {pos}: expected {ref}, found {actual}")
                self.seq_array['nt'][idx:idx + length] = np.frombuffer(alt.encode(), dtype='S1')

        # 2) Bulk insertions
        if ins:
            ins.sort(key=lambda x: x[0])
            positions = np.array([p for p, _ in ins], dtype=coords.dtype)
            idxs = np.searchsorted(coords, positions)
            new_rows = []
            for (pos, alt), idx in zip(ins, idxs):
                cnt = self.insertion_counters[pos]
                eps = 1e-6
                for i, nt in enumerate(alt):
                    new_idx = pos + (cnt + i + 1) * eps
                    new_rows.append((nt.encode(), new_idx, b'-', np.nan, True))
                self.insertion_counters[pos] += len(alt)
            merged = np.concatenate([self.seq_array, np.array(new_rows, dtype=self.seq_array.dtype)])
            merged.sort(order='index')
            self.seq_array = merged

        # 3) Bulk deletions
        if dels:
            dels.sort(key=lambda x: x[0])
            positions = np.array([p for p, _ in dels], dtype=coords.dtype)
            idxs = np.searchsorted(self.seq_array['index'], positions)
            mask = np.ones(len(self.seq_array), dtype=bool)
            for (pos, ref), idx in zip(dels, idxs):
                length = len(ref)
                mask[idx:idx + length] = False
            self.seq_array = self.seq_array[mask]

        # Finalize valid mask
        self.seq_array['valid_mask'] = self.seq_array['nt'] != b'-'
        return self

    def complement(self) -> SeqMat:
        comp = {b'A': b'T', b'T': b'A', b'C': b'G', b'G': b'C', b'-': b'-'}
        nts = np.array([comp[x] for x in self.seq_array['nt']], dtype='S1')
        new = self.clone()
        new.seq_array['nt'] = nts
        return new

    def reverse_complement(self) -> SeqMat:
        new = self.complement().clone()
        new.seq_array = new.seq_array[::-1].copy()
        new.rev = not self.rev
        return new

    def __getitem__(self, key: Union[int, slice]) -> np.ndarray:
        coords = self.seq_array['index']
        if isinstance(key, int):
            idx = np.searchsorted(coords, key)
            if idx >= len(coords) or coords[idx] != key:
                raise KeyError(f"Position {key} not found.")
            return self.seq_array[idx]
        if isinstance(key, slice):
            start = key.start or coords.min()
            stop = key.stop or coords.max()
            mask = (coords >= start) & (coords <= stop)
            return self.seq_array[mask]
        raise TypeError("Invalid index type.")
