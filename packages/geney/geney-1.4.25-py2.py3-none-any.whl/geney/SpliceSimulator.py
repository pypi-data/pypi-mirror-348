import numpy as np
import pandas as pd
from collections import defaultdict
from typing import List, Tuple, Dict, Generator, Any
from pandas import Series
from .utils.utils import short_hash_of_list


class SpliceSimulator:
    def __init__(self, splicing_df: pd.DataFrame, transcript, max_distance: int, feature='event'):
        """
        Initializes the SpliceSimulator.

        Args:
            splicing_df (pd.DataFrame): DataFrame containing splicing information.
                Expected to have columns 'donors' and 'acceptors', each providing
                a list of tuples (position, probability).
            event_map: Additional event mapping information.
            rev (bool): Indicates whether the orientation is reversed.
            transcript_start (int): Start position of the transcript.
            transcript_end (int): End position of the transcript.
            max_distance (int): Maximum allowable distance for connecting splice sites.
        """
        self.full_df = splicing_df
        self.feature = feature
        self.rev = transcript.rev
        self.transcript_start = transcript.transcript_start
        self.transcript_end = transcript.transcript_end
        self.donors = transcript.donors
        self.acceptors = transcript.acceptors
        self.transcript = transcript
        self.max_distance = max_distance

        # Build sorted node lists from DataFrame columns.
        self.set_donor_nodes()
        self.set_acceptor_nodes()

    def _compute_splice_df(self, site_type: str) -> pd.DataFrame:
        """
        Generic method to compute donor or acceptor DataFrame with delta calculations and priority scores.

        Args:
            site_type (str): 'donor' or 'acceptor'
            feature (str): prefix of the feature column (e.g., 'mut1' → 'mut1_prob')

        Returns:
            pd.DataFrame: Annotated and scored splice site DataFrame
        """
        feature_col = f'{self.feature}_prob'
        df = getattr(self.full_df, site_type + 's').copy()
        site_set = getattr(self, site_type + 's')

        # Ensure all known sites are included
        missing = set(site_set) - set(df.index)
        if missing:
            df = pd.concat([df, pd.DataFrame(index=list(missing))], axis=0)
            df.loc[list(missing), ['annotated', 'ref_prob', feature_col]] = [True, 1, 1]

        # Ensure 'annotated' column exists and is boolean
        if 'annotated' not in df.columns:
            df['annotated'] = False
        else:
            df['annotated'] = df['annotated'].where(df['annotated'].notna(), False).astype(bool)

        # Sort by genomic position (respect strand orientation)
        df.sort_index(ascending=not self.rev, inplace=True)

        # === DELTA COMPUTATIONS ===
        MIN_INCREASE_RATIO = 0.2

        df['discovered_delta'] = np.where(
            ~df['annotated'],
            (df[feature_col] - df['ref_prob']),
            np.nan
        )
        df['discovered_delta'] = df['discovered_delta'].where(df['discovered_delta'] >= MIN_INCREASE_RATIO, 0)

        with np.errstate(divide='ignore', invalid='ignore'):
            df['deleted_delta'] = np.where(
                (df['ref_prob'] > 0) & df['annotated'],
                (df[feature_col] - df['ref_prob']) / df['ref_prob'],
                0
            )
        df['deleted_delta'] = df['deleted_delta'].clip(upper=0)

        df['P'] = df['annotated'].astype(float) + df['discovered_delta'] + df['deleted_delta']
        return df

    @property
    def donor_df(self) -> pd.DataFrame:
        return self._compute_splice_df('donor')

    @property
    def acceptor_df(self) -> pd.DataFrame:
        return self._compute_splice_df('acceptor')

    def report(self, pos):
        metadata = self.find_splice_site_proximity(pos)
        metadata['donor_events'] = self.donor_df[
            (self.donor_df.deleted_delta.abs() > 0.2) | (
                        self.donor_df.discovered_delta.abs() > 0.2)].reset_index().to_json()
        metadata['acceptor_events'] = self.acceptor_df[(self.acceptor_df.deleted_delta.abs() > 0.2) | (
                self.acceptor_df.discovered_delta.abs() > 0.2)].reset_index().to_json()
        metadata['missplicing'] = self.max_splicing_delta('event_prob')
        return metadata

    def max_splicing_delta(self, event) -> pd.Series:
        """
        Computes the maximum missplicing delta for both donor and acceptor sites.

        Args:
            event: The event column to compare against the reference.

        Returns:

            pd.Series: A series with keys 'donor' and 'acceptor' containing the maximum differences.
        """
        all_diffs = []

        for site_type in ['donors', 'acceptors']:
            df = self.full_df[site_type]
            diffs = (df[event] - df['ref_prob']).tolist()
            all_diffs.extend(diffs)

        # max(..., key=abs) picks the element whose absolute value is largest
        max_diff = max(all_diffs, key=abs)
        return max_diff

    def set_donor_nodes(self) -> None:
        """
        Builds a sorted list of donor nodes.
        A working copy is made from the donors property; then the transcript_end is appended as
        a candidate with a full (1) probability. The list is sorted based on the position and probability.
        """
        donors = self.donor_df.P
        donor_list = list(donors[donors > 0].round(2).items())  # Each tuple is (position, P)
        donor_list.append((self.transcript_end, 1))
        self.donor_nodes = sorted(
            donor_list,
            key=lambda x: int(x[0]),
            reverse=bool(self.rev)
        )

    def set_acceptor_nodes(self) -> None:
        """
        Builds a sorted list of acceptor nodes.
        """
        acceptors = self.acceptor_df.P
        acceptor_list = list(acceptors[acceptors > 0].round(2).items())  # Each tuple is (position, P)
        acceptor_list.insert(0, (self.transcript_start, 1.0))  # starting point
        self.acceptor_nodes = sorted(
            acceptor_list,
            key=lambda x: int(x[0]),
            reverse=bool(self.rev)
        )

    def generate_graph(self) -> Dict[Tuple[int, str], List[Tuple[int, str, float]]]:
        """
        Builds a directed graph (as an adjacency list) where keys are nodes (position, type)
        and values are lists of downstream connections as tuples:
            (next_position, next_type, adjusted_probability)

        The construction is done in three steps:
          1. Connect each donor node to acceptor nodes within max_distance.
          2. Connect each acceptor node to donor nodes within max_distance.
          3. Connect the transcript_start to donor nodes within max_distance.

        Returns:
            Dict: The adjacency list representing possible splice site transitions.
        """
        adjacency_list = defaultdict(list)

        # 1. Connect each donor node to nearby acceptor nodes.
        for d_pos, d_prob in self.donor_nodes:
            running_prob = 1
            for a_pos, a_prob in self.acceptor_nodes:
                correct_orientation = ((a_pos > d_pos and not self.rev) or
                                       (a_pos < d_pos and self.rev))
                distance_valid = abs(a_pos - d_pos) <= self.max_distance
                if correct_orientation and distance_valid:
                    if not self.rev:
                        in_between_acceptors = sum(1 for a, _ in self.acceptor_nodes if d_pos < a < a_pos)
                        in_between_donors = sum(1 for d, _ in self.donor_nodes if d_pos < d < a_pos)
                    else:
                        in_between_acceptors = sum(1 for a, _ in self.acceptor_nodes if a_pos < a < d_pos)
                        in_between_donors = sum(1 for d, _ in self.donor_nodes if a_pos < d < d_pos)

                    if in_between_donors == 0 or in_between_acceptors == 0:
                        adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob))
                        running_prob -= a_prob
                    else:
                        if running_prob > 0:
                            adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob * running_prob))
                            running_prob -= a_prob
                        else:
                            break

        # 2. Connect each acceptor node to nearby donor nodes.
        for a_pos, a_prob in self.acceptor_nodes:
            running_prob = 1
            for d_pos, d_prob in self.donor_nodes:
                correct_orientation = ((d_pos > a_pos and not self.rev) or
                                       (d_pos < a_pos and self.rev))
                distance_valid = abs(d_pos - a_pos) <= self.max_distance
                if correct_orientation and distance_valid:
                    if not self.rev:
                        in_between_acceptors = sum(1 for a, _ in self.acceptor_nodes if a_pos < a < d_pos)
                        in_between_donors = sum(1 for d, _ in self.donor_nodes if a_pos < d < d_pos)
                    else:
                        in_between_acceptors = sum(1 for a, _ in self.acceptor_nodes if d_pos < a < a_pos)
                        in_between_donors = sum(1 for d, _ in self.donor_nodes if d_pos < d < a_pos)
                    tag = 'donor' if d_pos != self.transcript_end else 'transcript_end'
                    if in_between_acceptors == 0:
                        adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob))
                        running_prob -= d_prob
                    else:
                        if running_prob > 0:
                            adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob * running_prob))
                            running_prob -= d_prob
                        else:
                            break

        # 3. Connect transcript_start to donor nodes within max_distance.
        running_prob = 1
        for d_pos, d_prob in self.donor_nodes:
            correct_orientation = ((d_pos > self.transcript_start and not self.rev) or
                                   (d_pos < self.transcript_start and self.rev))
            distance_valid = abs(d_pos - self.transcript_start) <= self.max_distance
            if correct_orientation and distance_valid:
                adjacency_list[(self.transcript_start, 'transcript_start')].append((d_pos, 'donor', d_prob))
                running_prob -= d_prob
                if running_prob <= 0:
                    break

        # Normalize each outgoing edge list so that probabilities sum to 1.
        for key, next_nodes in adjacency_list.items():
            total_prob = sum(prob for (_, _, prob) in next_nodes)
            if total_prob > 0:
                adjacency_list[key] = [(pos, typ, round(prob / total_prob, 3))
                                       for pos, typ, prob in next_nodes]
        return adjacency_list

    def find_all_paths(self,
                       graph: Dict[Tuple[int, str], List[Tuple[int, str, float]]],
                       start: Tuple[int, str],
                       end: Tuple[int, str],
                       path: List[Tuple[int, str]] = None,
                       probability: float = 1.0) -> Generator[Tuple[List[Tuple[int, str]], float], None, None]:
        """
        Recursively traverses the graph to yield all complete paths from start to end.

        Args:
            graph (Dict): The adjacency list graph.
            start (Tuple[int, str]): The current node.
            end (Tuple[int, str]): The target node.
            path (List[Tuple[int, str]], optional): The current path. Defaults to None.
            probability (float, optional): The cumulative probability along the current path.

        Yields:
            Generator yielding tuples of (path, cumulative_probability).
        """
        if path is None:
            path = [start]
        else:
            path = path + [start]
        if start == end:
            yield path, probability
            return
        if start not in graph:
            return
        for next_node, node_type, prob in graph[start]:
            yield from self.find_all_paths(graph, (next_node, node_type), end, path, probability * prob)

    def get_viable_paths(self) -> List[Tuple[List[Tuple[int, str]], float]]:
        """
        Generates and returns all complete splice-site paths (from transcript_start to transcript_end),
        sorted by overall likelihood in descending order.

        Returns:
            List[Tuple[List[Tuple[int, str]], float]]: Each tuple contains a path (list of (position, type))
            and its overall probability.
        """
        graph = self.generate_graph()
        start_node = (self.transcript_start, 'transcript_start')
        end_node = (self.transcript_end, 'transcript_end')
        paths = list(self.find_all_paths(graph, start_node, end_node))
        paths.sort(key=lambda x: x[1], reverse=True)
        return paths

    def get_viable_transcripts(self, metadata=False) -> Generator[tuple[Any, Series] | Any, Any, None]:
        """
        Returns a list of transcript-like objects cloned from `self.transcript`,
        each representing a valid splice path with updated donor/acceptor sites,
        total path probability, and a unique hash based on exon/intron structure.
        """
        graph = self.generate_graph()
        start_node = (self.transcript_start, 'transcript_start')
        end_node = (self.transcript_end, 'transcript_end')

        paths = list(self.find_all_paths(graph, start_node, end_node))
        paths.sort(key=lambda x: x[1], reverse=True)

        viable_transcripts = []

        for path, prob in paths:
            donors = [pos for pos, typ in path if typ == 'donor']
            acceptors = [pos for pos, typ in path if typ == 'acceptor']

            transcript = self.transcript.clone()  # Make sure this creates a deep copy

            transcript.donors = [d for d in donors if d != transcript.transcript_end]
            transcript.acceptors = [a for a in acceptors if a != transcript.transcript_start]
            transcript.path_weight = prob
            transcript.path_hash = short_hash_of_list(tuple(donors + acceptors))  # or use a better hash function if needed
            transcript.generate_mature_mrna().generate_protein()
            if metadata:
                md = pd.concat([self.compare_splicing_to_reference(transcript), pd.Series({'isoform_prevalence': transcript.path_weight, 'isoform_id': transcript.path_hash})])
                yield transcript, md
            else:
                yield transcript

    def find_splice_site_proximity(self, pos):
        def result(region, index, start, end):
            return pd.Series({
                'region': region,
                'index': index + 1,
                "5'_dist": abs(pos - min(start, end)),
                "3'_dist": abs(pos - max(start, end))
            })

        if not hasattr(self.transcript, 'exons') or not hasattr(self.transcript, 'introns'):
            return pd.Series({'region': None, 'index': None, "5'_dist": np.inf, "3'_dist": np.inf})

        for i, (start, end) in enumerate(self.transcript.exons):
            if min(start, end) <= pos <= max(start, end):
                return result('exon', i, start, end)

        for i, (start, end) in enumerate(self.transcript.introns):
            if min(start, end) <= pos <= max(start, end):
                return result('intron', i, start, end)

        return pd.Series({'region': None, 'index': None, "5'_dist": np.inf, "3'_dist": np.inf})


    def define_missplicing_events(self, var):
        """
        Compares a reference transcript and a variant to detect splicing abnormalities.
        Returns string descriptions of each type of missplicing event.
        """

        ref = self.transcript
        ref_introns, ref_exons = getattr(ref, 'introns', []), getattr(ref, 'exons', [])
        var_introns, var_exons = getattr(var, 'introns', []), getattr(var, 'exons', [])

        num_ref_exons = len(ref_exons)
        num_ref_introns = len(ref_introns)

        pes = []
        pir = []
        es = []
        ne = []
        ir = []

        for exon_count, (t1, t2) in enumerate(ref_exons):
            for (s1, s2) in var_exons:
                if not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)) or \
                   (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2))):
                    pes.append(f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}')

        for intron_count, (t1, t2) in enumerate(ref_introns):
            for (s1, s2) in var_introns:
                if not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)) or \
                   (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2))):
                    pir.append(f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}')

        for exon_count, (t1, t2) in enumerate(ref_exons):
            if t1 not in var.acceptors and t2 not in var.donors:
                es.append(f'Exon {exon_count + 1}/{num_ref_exons} skipped: {(t1, t2)}')

        for (s1, s2) in var_exons:
            if s1 not in ref.acceptors and s2 not in ref.donors:
                ne.append(f'Novel Exon: {(s1, s2)}')

        for intron_count, (t1, t2) in enumerate(ref_introns):
            if t1 not in var.donors and t2 not in var.acceptors:
                ir.append(f'Intron {intron_count + 1}/{num_ref_introns} retained: {(t1, t2)}')

        return ','.join(pes), ','.join(pir), ','.join(es), ','.join(ne), ','.join(ir)


    def summarize_missplicing_event(self, pes, pir, es, ne, ir):
        """
        Given raw missplicing event strings, returns a compact classification tag.
        """
        event = []
        if pes: event.append('PES')
        if es:  event.append('ES')
        if pir: event.append('PIR')
        if ir:  event.append('IR')
        if ne:  event.append('NE')
        return ','.join(event) if event else '-'

    def compare_splicing_to_reference(self, transcript_variant):
        pes, pir, es, ne, ir = self.define_missplicing_events(transcript_variant)
        return pd.Series({
            'pes': pes,
            'pir': pir,
            'es': es,
            'ne': ne,
            'ir': ir,
            'summary': self.summarize_missplicing_event(pes, pir, es, ne, ir)
        })