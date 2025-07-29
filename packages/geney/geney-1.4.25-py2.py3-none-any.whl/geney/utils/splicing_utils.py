# __all__ = ['run_splicing_engine', 'adjoin_splicing_outcomes', 'process_epistasis']

import pandas as pd
from typing import List, Tuple

def run_splicing_engine(seq: str, engine: str = 'spliceai') -> Tuple[List[float], List[float]]:
    """
    Run the specified splicing engine to predict splice site probabilities on a sequence.

    Args:
        seq: Nucleotide sequence.
        engine: Engine name ('spliceai' or 'pangolin').

    Returns:
        Tuple (donor_probs, acceptor_probs) as lists of probability values.

    Raises:
        ValueError: If the engine is not implemented.
    """
    match engine:
        case 'spliceai':
            from geney.utils.spliceai_utils import sai_predict_probs, sai_models
            # print(seq)
            acceptor_probs, donor_probs = sai_predict_probs(seq, models=sai_models)
        case 'pangolin':
            from geney.utils.pangolin_utils import pangolin_predict_probs, pang_models
            # print(seq)
            donor_probs, acceptor_probs = pangolin_predict_probs(seq, models=pang_models)
        case _:
            raise ValueError(f"Engine '{engine}' not implemented")

    return donor_probs, acceptor_probs



def adjoin_splicing_outcomes(splicing_predictions, transcript=None):
    """
    Predicts splicing effect for multiple mutations and organizes the output as a multi-index DataFrame.

    Args:
        mut_ids (dict): Dictionary where keys are mutation labels (e.g. 'mut1', 'mut2', 'epistasis') and
                        values are mutation strings in format 'GENE:CHR:POS:REF:ALT'.
        transcript (str): Transcript ID to target (optional).
        engine (str): Splicing engine (default: 'spliceai').

    Returns:
        pd.DataFrame: Multi-index column DataFrame with wild-type, canonical, and mutation-specific predictions.
    """
    dfs = []
    for label, splicing_df in splicing_predictions.items():
        var_df = splicing_df.rename(columns={
            'donor_prob': ('donors', f'{label}_prob'),
            'acceptor_prob': ('acceptors', f'{label}_prob'),
            'nucleotides': ('nts', f'{label}')
        })
        dfs.append(var_df)

    # Concatenate all DataFrames and unify columns
    full_df = pd.concat(dfs, axis=1)

    # Ensure MultiIndex columns
    if not isinstance(full_df.columns, pd.MultiIndex):
        full_df.columns = pd.MultiIndex.from_tuples(full_df.columns)

    if transcript is not None:
        full_df[('acceptors', 'annotated')] = full_df.apply(
            lambda row: row.name in transcript.acceptors,
            axis=1
        )

        full_df[('donors', 'annotated')] = full_df.apply(
            lambda row: row.name in transcript.donors,
            axis=1
        )

        full_df.sort_index(axis=1, level=0, inplace=True)
        full_df.sort_index(ascending=not transcript.rev, inplace=True)
    else:
        full_df.sort_index(axis=1, level=0, inplace=True)

    return full_df


def process_epistasis(df: pd.DataFrame, threshold=0.25) -> pd.DataFrame:
    """
    Computes the expected epistasis effect (additive) and residual epistasis
    for both donor and acceptor probabilities.

    Adds new columns under donors and acceptors:
        - expected_epistasis
        - residual_epistasis

    Args:
        df (pd.DataFrame): MultiIndex column DataFrame with keys:
            'wt_prob', 'mut1_prob', 'mut2_prob', 'epistasis_prob'

    Returns:
        pd.DataFrame: Modified DataFrame with expected and residual epistasis columns added.
    """
    for feature in ['donors', 'acceptors']:
        wt = df[feature]['wt_prob']
        mut1 = df[feature]['mut1_prob']
        mut2 = df[feature]['mut2_prob']
        true_epi = df[feature]['epistasis_prob']

        expected = mut1 + mut2 - wt
        residual = true_epi - expected

        df[(feature, 'expected_epistasis')] = expected
        df[(feature, 'residual_epistasis')] = residual

    df = df.sort_index(axis=1, level=0)
    mask = (
                   df['donors']['residual_epistasis'].abs() > threshold
           ) | (
                   df['acceptors']['residual_epistasis'].abs() > threshold
           )

    return df[mask]


# def predict_splicing(mut_id=None, transcript=None, engine='spliceai'):
#     gene = Gene.from_file(mut_id.split(':')[0]).transcript(transcript).generate_pre_mrna()
#     if mut_id is None:
#         pass
#     else:
#         for m in mut_id.split('|'):
#             gene.pre_mrna.apply_mutation(m)
#     gene.pre_mrna.set_name(mut_id)
#     return gene.pre_mrna.predict_missplicing(engine=engine, fmt='df')
#
#
#
#
#
#
# def find_event_splicing(mutations, engine='spliceai'):
#     data = epistasis_id.split('|')
#     gene = data[0].split(':')[0]
#     pos = int(sum([int(p.split(':')[2]) for p in data]) / 2)
#     g = Gene.from_file(gene).transcript().generate_pre_mrna()
#     transcript = g.clone().pre_mrna
#
#     muts = [MutSeqMat.from_mutid(m, g.rev) for m in data]
#     # if g.rev:
#     #     muts = [m.reverse_complement() for m in muts]
#
#     mut1 = transcript.clone().mutate(muts[0])
#     mut2 = transcript.clone().mutate(muts[1])
#     epistasis = transcript.clone()
#     for m in muts:
#         epistasis.mutate(m, inplace=True)
#
#     wild_type = transcript.predict_splicing(pos, engine=engine)
#     mut1 = mut1.predict_splicing(pos, engine=engine)
#     mut2 = mut2.predict_splicing(pos, engine=engine)
#     epistasis = epistasis.predict_splicing(pos, engine=engine)
#
#     combined = pd.concat([wild_type, mut1, mut2, epistasis], axis=1, keys=['wild_type', 'mut1', 'mut2', 'epistasis'], join='outer')
#     return combined
#
# # def extract_epistatic_sites(df, site_type_col='site_type', threshold=0.25):
# #     """
# #     From a multi-index DataFrame with columns like ('wild_type', 'donor_prob'), etc.,
# #     compute expected additive effect and epistatic residual for donor and acceptor probabilities.
# #     Return only rows where:
# #         1. |residual| > threshold
# #         2. donor sites have site_type == 1, acceptor sites have site_type == 0
# #     """
# #     features = ['donor_prob', 'acceptor_prob']
# #     expected = {}
# #     residual = {}
# #
# #     for feature in features:
# #         wt = df[('wild_type', feature)]
# #         mut1 = df[('mut1', feature)]
# #         mut2 = df[('mut2', feature)]
# #         epi = df[('epistasis', feature)]
# #
# #         expected_feature = 3 * wt - mut1 - mut2
# #         residual_feature = expected_feature - epi
# #
# #         expected[('expected', feature)] = expected_feature
# #         residual[('residual', feature)] = residual_feature
# #
# #     # Combine new columns
# #     expected_df = pd.DataFrame(expected)
# #     residual_df = pd.DataFrame(residual)
# #
# #     # Join to original
# #     df_combined = pd.concat([df, expected_df, residual_df], axis=1)
# #
# #     # Create mask based on residual threshold
# #     mask = (
# #         (residual_df.abs() > threshold)
# #         .any(axis=1)  # at least one feature has large residual
# #     )
# #
# #     # Site type condition: donor=1, acceptor=0
# #     donor_mask = df[('wild_type', 'donor_prob')].notna() & (df[site_type_col] == 1)
# #     acceptor_mask = df[('wild_type', 'acceptor_prob')].notna() & (df[site_type_col] == 0)
# #
# #     # Combine all masks
# #     final_mask = mask & (donor_mask | acceptor_mask)
# #
# #     return df_combined[final_mask]
# #
# #
# # # variability = df.groupby(level=1, axis=1).apply(lambda subdf: subdf.max(axis=1) - subdf.min(axis=1))
# #
#
# """
# splicing_module.py
#
# A modular and comprehensive implementation for splicing, missplicing, and pairwise epistasis analysis.
# This module has been refactored with advanced Python practices:
#   • Extensive type annotations and detailed docstrings.
#   • Decomposition into small, testable functions and classes.
#   • Explicit encapsulation of the pairwise epistasis analysis.
#   • Usage of Python 3.10+ pattern matching for engine dispatch.
#
# Dependencies:
#     numpy, pandas, sqlite3, json, os, redis, and internal modules: Gene, SeqMats, config, spliceai_utils, and pangolin_utils.
# """
#
# import os
# import json
# import sqlite3
# from collections import defaultdict
# from dataclasses import dataclass, field
# from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union
#
# import numpy as np
# import pandas as pd
# from redis import Redis
#
# # Internal module imports (assumed to be in the same package)
# from .Gene import Gene
# from .SeqMats import MutSeqMat
# from . import config
#
# # # Type aliases for clarity
# # SpliceProbs = Dict[int, float]
# # AdjacencyKey = Tuple[int, str]
# # AdjacencyValue = Tuple[int, str, float]
# # AdjacencyList = Dict[AdjacencyKey, List[AdjacencyValue]]
#
# def run_splicing_engine(seq: str, engine: str = 'spliceai') -> Tuple[List[float], List[float]]:
#     """
#     Run the specified splicing engine to predict splice site probabilities on a sequence.
#
#     Args:
#         seq: Nucleotide sequence.
#         engine: Engine name ('spliceai' or 'pangolin').
#
#     Returns:
#         Tuple (donor_probs, acceptor_probs) as lists of probability values.
#
#     Raises:
#         ValueError: If the engine is not implemented.
#     """
#     match engine:
#         case 'spliceai':
#             from .spliceai_utils import sai_predict_probs, sai_models
#             acceptor_probs, donor_probs = sai_predict_probs(seq, models=sai_models)
#         case 'pangolin':
#             from .pangolin_utils import pangolin_predict_probs, pang_models
#             donor_probs, acceptor_probs = pangolin_predict_probs(seq, models=pang_models)
#         case _:
#             raise ValueError(f"Engine '{engine}' not implemented")
#
#     return donor_probs, acceptor_probs
#
#
# # =============================================================================
# # Helper Functions
# # =============================================================================
#
# def generate_adjacency_list(
#         acceptors: List[Tuple[int, float]],
#         donors: List[Tuple[int, float]],
#         transcript_start: int,
#         transcript_end: int,
#         max_distance: int = 50,
#         rev: bool = False
# ) -> AdjacencyList:
#     """
#     Build an adjacency list from donors to acceptors (and vice versa) based on distance and orientation.
#
#     Args:
#         acceptors: List of tuples (position, probability) for acceptor sites.
#         donors: List of tuples (position, probability) for donor sites.
#         transcript_start: Start coordinate of the transcript.
#         transcript_end: End coordinate of the transcript.
#         max_distance: Maximum allowed distance to connect sites.
#         rev: If True, consider reverse orientation.
#
#     Returns:
#         A dictionary mapping (position, type) to a list of (neighbor_position, neighbor_type, normalized_probability).
#     """
#     # Append transcript end as an extra donor node
#     donors = donors + [(transcript_end, 1)]
#     # Sort acceptors and donors; use reversed ordering if needed
#     acceptors = sorted(acceptors, key=lambda x: (x[0], x[1] if not rev else -x[1]), reverse=rev)
#     donors = sorted(donors, key=lambda x: (x[0], x[1] if not rev else -x[1]), reverse=rev)
#
#     adjacency_list: AdjacencyList = defaultdict(list)
#
#     # Connect donors to acceptors
#     for d_pos, d_prob in donors:
#         running_prob = 1.0
#         for a_pos, a_prob in acceptors:
#             # Check orientation and max distance
#             correct_orientation = (a_pos > d_pos and not rev) or (a_pos < d_pos and rev)
#             distance_valid = abs(a_pos - d_pos) <= max_distance
#             if correct_orientation and distance_valid:
#                 # Count intervening sites as a simplified penalty
#                 in_between_acceptors = sum(1 for a, _ in acceptors if (d_pos < a < a_pos) if not rev else (
#                             a_pos < a < d_pos))
#                 in_between_donors = sum(1 for d, _ in donors if (d_pos < d < a_pos) if not rev else (a_pos < d < d_pos))
#                 # If one set is empty, use raw probability; otherwise use a running product
#                 if in_between_donors == 0 or in_between_acceptors == 0:
#                     adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob))
#                     running_prob -= a_prob
#                 elif running_prob > 0:
#                     adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob * running_prob))
#                     running_prob -= a_prob
#                 else:
#                     break
#
#     # Connect acceptors to donors
#     for a_pos, a_prob in acceptors:
#         running_prob = 1.0
#         for d_pos, d_prob in donors:
#             correct_orientation = (d_pos > a_pos and not rev) or (d_pos < a_pos and rev)
#             distance_valid = abs(d_pos - a_pos) <= max_distance
#             if correct_orientation and distance_valid:
#                 in_between_acceptors = sum(1 for a, _ in acceptors if (a_pos < a < d_pos) if not rev else (
#                             d_pos < a < a_pos))
#                 in_between_donors = sum(1 for d, _ in donors if (a_pos < d < d_pos) if not rev else (d_pos < d < a_pos))
#                 # Tag the donor as transcript_end if appropriate
#                 tag = 'donor' if d_pos != transcript_end else 'transcript_end'
#                 if in_between_acceptors == 0:
#                     adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob))
#                     running_prob -= d_prob
#                 elif running_prob > 0:
#                     adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob * running_prob))
#                     running_prob -= d_prob
#                 else:
#                     break
#
#     # Connect transcript start to donors
#     running_prob = 1.0
#     for d_pos, d_prob in donors:
#         if ((d_pos > transcript_start and not rev) or (d_pos < transcript_start and rev)) and abs(
#                 d_pos - transcript_start) <= max_distance:
#             adjacency_list[(transcript_start, 'transcript_start')].append((d_pos, 'donor', d_prob))
#             running_prob -= d_prob
#             if running_prob <= 0:
#                 break
#
#     # Normalize probabilities in each adjacency list
#     for key, next_nodes in adjacency_list.items():
#         total = sum(prob for _, _, prob in next_nodes)
#         if total > 0:
#             adjacency_list[key] = [(pos, typ, round(prob / total, 3)) for pos, typ, prob in next_nodes]
#
#     return dict(adjacency_list)
#
#
# def find_all_paths(
#         graph: AdjacencyList,
#         start: Tuple[int, str],
#         end: Tuple[int, str],
#         path: List[Tuple[int, str]] = [],
#         probability: float = 1.0
# ) -> Generator[Tuple[List[Tuple[int, str]], float], None, None]:
#     """
#     Recursively generate all paths from start node to end node in the graph.
#
#     Args:
#         graph: Adjacency list mapping nodes to neighbor nodes and probabilities.
#         start: The starting node (position, type).
#         end: The target node (position, type).
#         path: The path traversed so far.
#         probability: The cumulative probability along the path.
#
#     Yields:
#         A tuple of the complete path and its cumulative probability.
#     """
#     path = path + [start]
#     if start == end:
#         yield path, probability
#         return
#
#     if start not in graph:
#         return
#
#     for next_node, node_type, prob in graph[start]:
#         yield from find_all_paths(graph, (next_node, node_type), end, path, probability * prob)
#
#
# def prepare_splice_sites(
#         acceptors: List[int],
#         donors: List[int],
#         aberrant_splicing: Dict[str, Any]
# ) -> Tuple[List[Tuple[int, float]], List[Tuple[int, float]]]:
#     """
#     Prepare splice sites by merging reference sites with aberrant events.
#
#     Args:
#         acceptors: List of acceptor positions.
#         donors: List of donor positions.
#         aberrant_splicing: Dictionary containing aberrant splicing events.
#
#     Returns:
#         Tuple of lists:
#           - List of tuples (acceptor_position, probability)
#           - List of tuples (donor_position, probability)
#     """
#     acceptor_dict = {p: 1 for p in acceptors}
#     donor_dict = {p: 1 for p in donors}
#
#     for p, v in aberrant_splicing.get('missed_donors', {}).items():
#         donor_dict[p] = v['absolute']
#     for p, v in aberrant_splicing.get('discovered_donors', {}).items():
#         donor_dict[p] = v['absolute']
#     for p, v in aberrant_splicing.get('missed_acceptors', {}).items():
#         acceptor_dict[p] = v['absolute']
#     for p, v in aberrant_splicing.get('discovered_acceptors', {}).items():
#         acceptor_dict[p] = v['absolute']
#
#     # Ensure keys are integers
#     acceptors_list = [(int(k), float(v)) for k, v in acceptor_dict.items()]
#     donors_list = [(int(k), float(v)) for k, v in donor_dict.items()]
#     return acceptors_list, donors_list
#
#
# def develop_aberrant_splicing(
#         transcript: Any,
#         aberrant_splicing: Any
# ) -> Generator[Dict[str, Any], None, None]:
#     """
#     Generator of potential aberrant splicing paths based on the transcript and missplicing events.
#
#     If no aberrant events are provided, returns the original splice sites.
#
#     Args:
#         transcript: Transcript object containing splice site positions.
#         aberrant_splicing: Object with missplicing events.
#
#     Yields:
#         Dictionary with keys 'acceptors', 'donors', and 'path_weight'.
#     """
#     if not aberrant_splicing:
#         yield {
#             'acceptors': transcript.acceptors,
#             'donors': transcript.donors,
#             'path_weight': 1
#         }
#     else:
#         all_acceptors, all_donors = prepare_splice_sites(
#             transcript.acceptors, transcript.donors, aberrant_splicing.missplicing
#         )
#         adj_list = generate_adjacency_list(
#             all_acceptors,
#             all_donors,
#             transcript_start=transcript.transcript_start,
#             transcript_end=transcript.transcript_end,
#             max_distance=100000,
#             rev=transcript.rev
#         )
#         start_node = (transcript.transcript_start, 'transcript_start')
#         end_node = (transcript.transcript_end, 'transcript_end')
#         for path, prob in find_all_paths(adj_list, start_node, end_node):
#             yield {
#                 'acceptors': [node[0] for node in path if node[1] == 'acceptor'],
#                 'donors': [node[0] for node in path if node[1] == 'donor'],
#                 'path_weight': prob
#             }
#
#
# def find_ss_changes(
#         ref_dct: Dict[int, float],
#         mut_dct: Dict[int, float],
#         known_splice_sites: Union[List[int], np.ndarray],
#         threshold: float = 0.5
# ) -> Tuple[Dict[float, Dict[str, float]], Dict[float, Dict[str, float]]]:
#     """
#     Compare reference and mutant splice probabilities to detect significant site changes.
#
#     Args:
#         ref_dct: Dictionary of splice site probabilities for the reference sequence.
#         mut_dct: Dictionary of splice site probabilities for the mutant sequence.
#         known_splice_sites: List/array of positions that are known splice sites.
#         threshold: Minimum difference required to flag a significant change.
#
#     Returns:
#         A tuple (discovered, deleted) where:
#             - discovered: Positions with a positive delta and not known splice sites.
#             - deleted: Positions with a negative delta among known splice sites.
#     """
#     all_positions = set(ref_dct.keys()).union(mut_dct.keys())
#     delta_dict = {pos: mut_dct.get(pos, 0) - ref_dct.get(pos, 0) for pos in all_positions}
#
#     discovered = {
#         float(k): {
#             'delta': round(float(delta), 3),
#             'absolute': round(float(mut_dct.get(k, 0)), 3),
#             'reference': round(ref_dct.get(k, 0), 3)
#         }
#         for k, delta in delta_dict.items() if delta >= threshold and k not in known_splice_sites
#     }
#     deleted = {
#         float(k): {
#             'delta': round(float(delta), 3),
#             'absolute': round(float(mut_dct.get(k, 0)), 3),
#             'reference': round(ref_dct.get(k, 0), 3)
#         }
#         for k, delta in delta_dict.items() if -delta >= threshold and k in known_splice_sites
#     }
#     return discovered, deleted
#
#
#
