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


    def __len__(self) -> int:
        return int(self.seq_array["valid_mask"].sum())

    def __repr__(self):
        return f"<SeqMat: {self.seq}>"

    def __str__(self):
        return self.seq

    def get_metadata(self) -> dict:
        """Retrieve all metadata as a dictionary."""
        return {
            "name": self.name,
            "source": self.source,
            "version": self.version,
            "notes": self.notes
        }

    @property
    def seq(self) -> str:
        return self.seq_array['nt'][self.seq_array['valid_mask']].tobytes().decode()

    @property
    def index(self) -> np.ndarray:
        return self.seq_array['index'][self.seq_array['valid_mask']]

    @property
    def conservation(self) -> np.ndarray:
        return self.seq_array['cons'][self.seq_array['valid_mask']]

    @property
    def max_index(self) -> float:
        return self.seq_array["index"].max()

    @property
    def min_index(self) -> float:
        return self.seq_array["index"].min()

    @property
    def start(self) -> float:
        return self.min_index

    @property
    def end(self) -> float:
        return self.max_index

    @property
    def mutated_positions(self) -> np.ndarray:
        return (self.seq_array["ref"] != self.seq_array["nt"])[self.seq_array["valid_mask"]].astype(int)

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

    def cut_out(self, introns: List[Tuple[int, int]]) -> "SeqMat":
        """
        Splices out regions from the sequence corresponding to the given intron boundaries.

        Handles reverse-complemented sequences by interpreting introns in reverse as well.

        Args:
            introns (List[Tuple[int, int]]): List of (start, end) intron boundaries.
                                             These are always genomic (absolute) coordinates,
                                             regardless of strand direction.

        Returns:
            SeqMat: A new instance with the intron regions removed.
        """
        # In reverse orientation, flip intron direction for comparison
        if self.rev:
            introns = [(end, start) if start > end else (start, end) for (start, end) in introns]

        mask = np.ones(len(self.seq_array), dtype=bool)

        for start, end in introns:
            lo, hi = min(start, end) + 1, max(start, end) - 1
            mask &= ~((self.seq_array["index"] >= lo) & (self.seq_array["index"] <= hi))

        new_instance = self.clone()
        new_instance.seq_array = self.seq_array[mask].copy()
        return new_instance

    def open_reading_frame(self, tis: int) -> "SeqMat":
        """
        Extracts the open reading frame starting from the translation initiation site (TIS)
        until the first in-frame stop codon.

        Args:
            tis (int): Genomic position of the translation initiation site (start codon).

        Returns:
            SeqMat: A new SeqMat instance containing the ORF (from TIS to stop codon inclusive).
        """
        if tis not in self.seq_array["index"]:
            print(f"Warning: TIS position {tis} not found, returning default.")
            return self.clone(start=0, end=3)

        # Extract nucleotide sequence and indices starting from TIS
        mask = self.seq_array["index"] >= tis if not self.rev else self.seq_array["index"] <= tis
        coding_part = self.seq_array[mask]
        coding_seq = coding_part["nt"].tobytes().decode()

        # Read codons in-frame
        for i in range(0, len(coding_seq) - 2, 3):
            codon = coding_seq[i:i + 3]
            if codon in {"TAA", "TAG", "TGA"}:
                # Determine index range for this ORF
                start = coding_part["index"][0]
                stop = coding_part["index"][i + 2]
                lo, hi = sorted((start, stop))
                return self.clone(start=lo, end=hi)

        raise ValueError("No in-frame stop codon found after the TIS.")

    def predict_splicing(self, position: int, engine='spliceai', context=7500, inplace=False): #, reference_donors=None, reference_acceptors=None) -> pd.DataFrame:
        """
        Predict splicing probabilities at a given position using the specified engine.

        Args:
            position (int): The genomic position to predict splicing probabilities for.
            engine (str): The prediction engine to use. Supported: 'spliceai', 'pangolin'.
            context (int): The length of the target central region (default: 7500).
            format (str): Output format for the splicing engine results.

        Returns:
            pd.DataFrame: A DataFrame containing:
                - position: The genomic position
                - donor_prob: Probability of being a donor splice site
                - acceptor_prob: Probability of being an acceptor splice site
                - nucleotides: The nucleotide sequence at that position

        Raises:
            ValueError: If an unsupported engine is provided.
            IndexError: If the position is not found in the sequence.
        """
        # Retrieve extended context (includes flanks) around the position.
        # seq, indices = self.get_context(position, context=context, padding='N')
        target = self.clone(position - context, position + context)
        # print(len(target.seq))
        seq, indices = target.seq, target.index
        # print(len(seq))
        # rel_pos = np.where(indices == position)[0][0]
        # print(rel_pos)
        rel_pos = np.abs(indices - position).argmin()
        # print(rel_pos, len(seq))
        left_missing, right_missing = max(0, context - rel_pos), max(0, context - (len(seq) - rel_pos))
        # print(left_missing, right_missing)
        if left_missing > 0 or right_missing > 0:
            step = -1 if self.rev else 1

            if left_missing > 0:
                left_pad = np.arange(indices[0] - step * left_missing, indices[0], step)
            else:
                left_pad = np.array([], dtype=indices.dtype)

            if right_missing > 0:
                right_pad = np.arange(indices[-1] + step, indices[-1] + step * (right_missing + 1), step)
            else:
                right_pad = np.array([], dtype=indices.dtype)

            seq = 'N' * left_missing + seq + 'N' * right_missing
            indices = np.concatenate([left_pad, indices, right_pad])

        # Run the splicing prediction engine (function assumed to be defined externally)
        from .splicing_utils import run_splicing_engine
        donor_probs, acceptor_probs = run_splicing_engine(seq, engine)
        # Trim off the fixed flanks before returning results.
        seq = seq[5000:-5000]
        indices = indices[5000:-5000]
        df = pd.DataFrame({
            'position': indices,
            'donor_prob': donor_probs,
            'acceptor_prob': acceptor_probs,
            'nucleotides': list(seq)
        }).set_index('position').round(3)
        # if reference_donors is not None:
        #     df['ref_donor'] = df.index.isin(reference_donors).astype(int)
        # if reference_acceptors is not None:
        #     df['ref_acceptor'] = df.index.isin(reference_acceptors).astype(int)

        df.attrs['name'] = self.name
        if inplace:
            self.predicted_splicing = df
            return self
        else:
            return df

