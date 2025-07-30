__all__ = ['is_monotonic', 'contains', 'unload_json', 'unload_pickle', 'dump_json', 'dump_pickle', 'generate_random_nucleotide_sequences']

import pickle
import json
# import re
# from pathlib import Path
from bisect import bisect_left
import hashlib

# def is_monotonic(A):
#     x, y = [], []
#     x.extend(A)
#     y.extend(A)
#     x.sort()
#     y.sort(reverse=True)
#     if (x == A or y == A):
#         return True
#     return False


# def available_genes(organism='hg38'):
#     from geney import config
#     annotation_path = config[organism]['MRNA_PATH'] / 'protein_coding'
#     return sorted(list(set([m.stem.split('_')[-1] for m in annotation_path.glob('*')])))


def contains(a, x):
    """returns true if sorted sequence `a` contains `x`"""
    i = bisect_left(a, x)
    return i != len(a) and a[i] == x


def unload_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def dump_json(file_path, payload):
    with open(file_path, 'w') as f:
        json.dump(payload, f)
    return None


def unload_pickle(file_path):

    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data


def dump_pickle(file_path, payload):
    with open(file_path, 'wb') as f:
        pickle.dump(payload, f)
    return None



def is_monotonic(A):
    return all(x <= y for x, y in zip(A, A[1:])) or all(x >= y for x, y in zip(A, A[1:]))



def generate_random_nucleotide_sequences(num_sequences, min_len=3, max_len=10):
    """
    Generate random sequences of nucleotides.

    Parameters:
        num_sequences (int): Number of sequences to generate.
        sequence_length (int): Length of each sequence.

    Returns:
        list: A list of random nucleotide sequences.
    """
    import random
    nucleotides = ['A', 'C', 'G', 'T']
    lengths = list(range(min_len, max_len))
    sequences = [
        ''.join(random.choices(nucleotides, k=random.choice(lengths)))
        for _ in range(num_sequences)
    ]
    return sequences



def short_hash_of_list(numbers, length=5):
    encoded = repr(numbers).encode('utf-8')
    full_hash = hashlib.sha256(encoded).hexdigest()
    return full_hash[:length]
