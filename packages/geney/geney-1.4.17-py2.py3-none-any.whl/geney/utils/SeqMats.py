__all__ = ['SeqMat', 'format_mut_id']


from __future__ import annotations
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
    _pos_to_idx: dict = field(default_factory=dict, init=False, repr=False)

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
        # Initialize metadata
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
        self.seq_array['cons'] = (np.zeros(L, dtype='f4') if conservation is None else conservation)
        self.seq_array['valid_mask'] = self.seq_array['nt'] != b'-'

        # Initialize helpers
        self.insertion_counters = defaultdict(int)
        self._build_index_map()

    def _build_index_map(self):
        """Rebuild position-to-index lookup."""
        self._pos_to_idx = {float(pos): i for i, pos in enumerate(self.seq_array['index'])}

    def __len__(self) -> int:
        return int(self.seq_array['valid_mask'].sum())

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
        # copy metadata
        new.name = self.name
        new.version = self.version
        new.source = self.source
        new.notes = self.notes.copy()
        new.rev = self.rev
        new.predicted_splicing = None
        new.insertion_counters = defaultdict(int)

        # slice or full copy
        if start is not None and end is not None:
            mask = (self.seq_array['index'] >= start) & (self.seq_array['index'] <= end)
            new.seq_array = self.seq_array[mask].copy()
        else:
            new.seq_array = self.seq_array.copy()

        new._build_index_map()
        return new

    def apply_mutation(self, pos: float, ref: str, alt: str, only_snps: bool = False) -> SeqMat:
        """Apply a single mutation to this SeqMat."""
        # reverse-complement context
        if self.rev:
            self.reverse_complement()

        # left-normalize
        while ref and alt and ref[0] == alt[0]:
            pos += 1
            ref = ref[1:] or '-'
            alt = alt[1:] or '-'

        # substitution
        if ref != '-' and alt != '-':
            if len(ref) != len(alt):
                raise ValueError("Substitution requires equal-length alleles.")
            idx = self._pos_to_idx.get(pos)
            if idx is None:
                raise KeyError(f"Position {pos} not found.")
            end = idx + len(ref)
            if end > len(self.seq_array):
                raise IndexError(f"Out of bounds at {pos}.")
            # verify reference
            ref_seg = self.seq_array['ref'][idx:end]
            if not np.array_equal(ref_seg, np.frombuffer(ref.encode(), dtype='S1')):
                raise ValueError(f"Ref mismatch at {pos}.")
            # assign alt
            self.seq_array['nt'][idx:end] = np.frombuffer(alt.encode(), dtype='S1')

        # insertion
        elif ref == '-' and alt != '-':
            if only_snps:
                return self
            idx = self._pos_to_idx.get(pos)
            if idx is None:
                raise KeyError(f"Position {pos} not found.")
            cnt = self.insertion_counters[pos]
            eps = 1e-6
            new_rows = []
            for i, nt in enumerate(alt):
                new_rows.append((nt.encode(),
                                 pos + (cnt + i + 1)*eps,
                                 b'-',
                                 np.nan,
                                 True))
            self._insert_rows(idx, new_rows)
            self.insertion_counters[pos] += len(alt)

        # deletion
        elif alt == '-' and ref != '-':
            if only_snps:
                return self
            idx = self._pos_to_idx.get(pos)
            if idx is None:
                raise KeyError(f"Position {pos} not found.")
            end = idx + len(ref)
            # verify
            ref_seg = self.seq_array['ref'][idx:end]
            if not np.array_equal(ref_seg, np.frombuffer(ref.encode(), dtype='S1')):
                raise ValueError(f"Ref mismatch at {pos}.")
            self.seq_array = np.delete(self.seq_array, np.s_[idx:end])

        else:
            raise ValueError("Unsupported mutation type.")

        # update mask & index map
        self.seq_array['valid_mask'] = self.seq_array['nt'] != b'-'
        self._build_index_map()

        # restore orientation
        if self.rev:
            self.reverse_complement()
        return self

    def _insert_rows(self, idx: int, rows: List[tuple]):
        """Helper to insert new rows efficiently and resort."""
        arr = self.seq_array.tolist()
        arr[idx:idx] = rows
        new = np.array(arr, dtype=self.seq_array.dtype)
        new.sort(order='index')
        self.seq_array = new

    def complement(self) -> SeqMat:
        comp = {b'A':b'T', b'T':b'A', b'C':b'G', b'G':b'C', b'-':b'-'}
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
        idx = None
        if isinstance(key, int):
            idx = self._pos_to_idx.get(float(key))
            if idx is None:
                raise KeyError(f"Position {key} not found.")
            return self.seq_array[idx]
        if isinstance(key, slice):
            start = key.start or self.min_index
            stop = key.stop or self.max_index
            mask = (self.seq_array['index'] >= start) & (self.seq_array['index'] <= stop)
            return self.seq_array[mask]
        raise TypeError("Invalid index type.")
