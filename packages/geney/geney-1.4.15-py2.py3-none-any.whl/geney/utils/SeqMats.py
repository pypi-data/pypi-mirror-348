__all__ = ['SeqMat', 'format_mut_id']

from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional, Union, List, Tuple
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
    # Metadata fields (uncomment and/or extend as needed)
    name: str = field(default="Unnamed Sequence", metadata={"description": "Name of the sequence"})
    version: str = field(default="1.0", metadata={"description": "Version of the dataset"})
    source: str = field(default="Unknown", metadata={"description": "Source of the sequence data"})
    notes: dict = field(default_factory=dict, metadata={"description": "User-defined metadata dictionary"})

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
        self.predicted_splicing = None
        nucleotides = np.array(list(nucleotides))
        L = nucleotides.shape[0]
        if index.shape[0] != L:
            raise ValueError("Indices array length must match nucleotide sequence length.")
        if conservation is not None and conservation.shape[0] != L:
            raise ValueError("Conservation vector length must match sequence length.")
        if reference_nucleotides is not None and reference_nucleotides.shape[0] != L:
            raise ValueError("Reference nucleotide vector length must match sequence length.")

        dtype = np.dtype([
            ("nt", "S1"),
            ("index", np.float64),
            ("ref", "S1"),
            ("cons", np.float32),
            ("valid_mask", bool),
        ])

        self.seq_array = np.empty(L, dtype=dtype)
        self.seq_array["nt"] = nucleotides
        # Use provided reference nucleotides if available.
        self.seq_array["ref"] = nucleotides if reference_nucleotides is None else reference_nucleotides
        self.seq_array["index"] = index
        self.seq_array["cons"] = np.nan if conservation is None else conservation
        self.seq_array["valid_mask"] = self.seq_array["nt"] != b"-"
        self.insertion_counters = defaultdict(int)
        self._pos_to_idx = {pos: i for i, pos in enumerate(self.seq_array["index"])}

        self.source = source if source is not None else "Unknown"
        self.notes = notes if notes is not None else {}
        self.name = name
        self.rev = rev
        self.version = version

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
        return self.seq_array["nt"][self.seq_array["valid_mask"]].tobytes().decode()

    @property
    def index(self) -> np.ndarray:
        return self.seq_array["index"][self.seq_array["valid_mask"]]

    @property
    def conservation(self) -> np.ndarray:
        return self.seq_array["cons"][self.seq_array["valid_mask"]]

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

    def clone(self, start: Optional[int] = None, end: Optional[int] = None) -> "SeqMat":
        cloned = SeqMat.__new__(SeqMat)
        if start is not None and end is not None:
            cloned.seq_array = self.seq_array[(self.seq_array["index"] >= start) & (self.seq_array["index"] <= end)]
        else:
            cloned.seq_array = self.seq_array.copy()
        cloned.insertion_counters = defaultdict(int)
        cloned.name = self.name
        cloned.source = self.source
        cloned.version = self.version
        cloned.notes = self.notes.copy()
        cloned.rev = self.rev

        cloned._pos_to_idx = {pos: i for i, pos in enumerate(cloned.seq_array["index"])}

        return cloned

    def apply_mutation(self, pos: int, ref: str, alt: str, only_snps: bool = False):
        """
        Applies a mutation (SNP, substitution, insertion, or deletion) to the sequence.

        Parameters:
            pos (int): The reference position where the mutation should occur.
            ref (str): The reference allele (use '-' for insertions).
            alt (str): The alternate allele (use '-' for deletions).
            only_snps (bool): If True, only SNP substitutions are allowed; indels are ignored.

        Returns:
            SeqMat: The mutated sequence matrix.

        The method normalizes the mutation (dropping any shared prefix) and then applies:
         - A SNP/substitution if both alleles are non-gap.
         - An insertion if ref is '-' (after normalization).
         - A deletion if alt is '-' (after normalization).

        For insertions, new rows are added with fractional indices computed from an insertion counter.
        For deletions, the corresponding rows are removed.
        """
        return_to_rc = False
        if self.rev:
            return_to_rc = True
            self.reverse_complement()

        # Normalize shared prefix (similar to left-alignment in VCFs)
        while ref and alt and ref[0] == alt[0]:
            pos += 1
            ref = ref[1:] or "-"
            alt = alt[1:] or "-"

        # Case 1: SNP or multi-base substitution
        if ref != "-" and alt != "-":
            if len(ref) != len(alt):
                raise ValueError("Substitution mutations must have alleles of equal length.")

            # pos_idx = np.searchsorted(self.seq_array["index"], pos)
            pos_idx = self._pos_to_idx.get(pos)

            if pos_idx is None:
                raise ValueError(f"Position {pos} not found in index")

            end_idx = pos_idx + len(ref)
            if end_idx > len(self.seq_array):
                raise ValueError(f"Substitution range exceeds sequence length at position {pos}.")

            segment = self.seq_array["ref"][pos_idx:end_idx].tobytes().decode()
            if segment != ref:
                raise ValueError(f"Reference mismatch at position {pos}: expected '{ref}', found '{segment}'")

            # ref_segment = self.seq_array["ref"][pos_idx:end_idx]
            # expected_segment = np.frombuffer(ref.encode(), dtype='S1')
            # if not np.all(ref_segment == np.frombuffer(ref.encode(), dtype='S1')):
            #     actual_str = ref_segment.tobytes().decode()
            #     raise ValueError(f"Reference mismatch at position {pos}: expected '{ref}', found '{actual_str}'")
            # self.seq_array["nt"][pos_idx:end_idx] = np.frombuffer(alt.encode(), dtype='S1')

            for i, nt in enumerate(alt):
                self.seq_array["nt"][pos_idx + i] = nt.encode()

        # Case 2: Insertion (ref is '-' means nothing was present, and we need to add bases)
        elif ref == "-" and alt != "-":
            if only_snps:
                return self  # Skip if indels are not allowed.
            pos_idx = np.searchsorted(self.seq_array["index"], pos)
            insertion_count = self.insertion_counters[pos]
            eps = 1e-6
            new_rows = []
            for i, nt in enumerate(alt):
                new_index = pos + (insertion_count + i + 1) * eps
                new_row = (nt.encode(), new_index, b"-", np.float32(np.nan), True)
                new_rows.append(new_row)
            rows = list(self.seq_array)
            rows.extend(new_rows)
            new_seq_array = np.array(rows, dtype=self.seq_array.dtype)
            new_seq_array.sort(order="index")
            self.seq_array = new_seq_array
            self.insertion_counters[pos] += len(alt)

        # Case 3: Deletion (alt is '-' means bases are to be removed)
        elif alt == "-" and ref != "-":
            if only_snps:
                return self  # Skip if indels are not allowed.
            pos_idx = np.searchsorted(self.seq_array["index"], pos)
            end_idx = pos_idx + len(ref)
            if end_idx > len(self.seq_array):
                raise ValueError(f"Deletion range exceeds sequence length at position {pos}.")
            segment = self.seq_array["ref"][pos_idx:end_idx].tobytes().decode()
            if segment != ref:
                raise ValueError(
                    f"Reference mismatch for deletion at position {pos}: expected '{ref}', found '{segment}'")
            self.seq_array = np.delete(self.seq_array, np.s_[pos_idx:end_idx])
        else:
            raise ValueError("Unsupported mutation type. Provide valid ref and alt values.")

        self.seq_array["valid_mask"] = self.seq_array["nt"] != b"-"
        if return_to_rc:
            self.reverse_complement()

        return self

    def __getitem__(self, key: Union[int, slice]) -> np.ndarray:
        if isinstance(key, int):
            pos_idx = np.where(self.seq_array["index"] == key)[0]
            if pos_idx.size == 0:
                raise IndexError(f"Position {key} not found in sequence.")
            return self.seq_array[pos_idx[0]]
        elif isinstance(key, slice):
            start, stop = key.start, key.stop
            if start is None:
                start = self.seq_array["index"].min()
            if stop is None:
                stop = self.seq_array["index"].max()
            return self.seq_array[(self.seq_array["index"] >= start) & (self.seq_array["index"] <= stop)]
        else:
            raise TypeError("Indexing must be an integer or a slice.")

    def complement(self) -> "SeqMat":
        comp_dict = {b"A": b"T", b"T": b"A", b"C": b"G", b"G": b"C", b"-": b"-", b"N": b"N"}
        comp_seq = np.array([comp_dict[nt] for nt in self.seq_array["nt"]], dtype="S1")
        new_instance = self.clone()
        new_instance.seq_array["nt"] = comp_seq
        return new_instance

    def reverse_complement(self) -> "SeqMat":
        rev_comp_seq = self.complement().seq_array[::-1]
        self.seq_array = rev_comp_seq.copy()
        self.rev = not self.rev
        return self

    # def splice_out(self, introns: List[Tuple[int, int]]) -> "SeqMat":
    #     """
    #     Splices out regions from the sequence corresponding to the given intron boundaries.
    #
    #     Args:
    #         introns (List[Tuple[int, int]]): List of (start, end) intron boundaries to remove.
    #                                          Coordinates should match the 'index' field.
    #
    #     Returns:
    #         SeqMat: A new instance with the intron regions removed.
    #     """
    #     mask = np.ones(len(self.seq_array), dtype=bool)
    #
    #     for start, end in introns:
    #         mask &= ~((self.seq_array["index"] >= start) & (self.seq_array["index"] <= end))
    #
    #     new_instance = self.clone()
    #     new_instance.seq_array = self.seq_array[mask].copy()
    #     return new_instance

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

