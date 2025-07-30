
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import sys
import numpy as np


import torch
from spliceai_pytorch import SpliceAI
model = SpliceAI.from_preconfigured('10k')


device = torch.device('cpu')
if sys.platform == 'darwin':
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

if sys.platform == 'linux':
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

print(f"SpliceAI loaded to {device}.")
model.to(device)


def one_hot_encode(seq: str) -> torch.Tensor:
    """
    One-hot encodes a nucleotide sequence into shape [L, 4] (A, C, G, T).
    Unknowns (N or other) are mapped to all-zero vectors.
    """
    map = np.array([
        [0, 0, 0, 0],  # index 0: unknown (N, etc.)
        [1, 0, 0, 0],  # A
        [0, 1, 0, 0],  # C
        [0, 0, 1, 0],  # G
        [0, 0, 0, 1],  # T
    ], dtype=np.float32)

    # Build mapping: ASCII values
    ascii_seq = np.frombuffer(seq.upper().encode("ascii"), dtype=np.uint8)

    # A=65, C=67, G=71, T=84 → map A/C/G/T to 1/2/3/4; others to 0
    code_map = np.zeros(128, dtype=np.uint8)
    code_map[ord('A')] = 1
    code_map[ord('C')] = 2
    code_map[ord('G')] = 3
    code_map[ord('T')] = 4

    indices = code_map[ascii_seq]  # shape [L]
    onehot = map[indices]          # shape [L, 4]

    return torch.tensor(onehot, dtype=torch.float32)

def sai_predict_probs(seq: str, model) -> list:
    '''
    Predicts the donor and acceptor junction probability of each
    NT in seq using SpliceAI.

    Let m:=2*sai_mrg_context + L be the input seq length. It is assumed
    that the input seq has the following structure:

          seq = |<sai_mrg_context NTs><L NTs><sai_mrg_context NTs>|

    The returned probability matrix is of size 2XL, where
    the first row is the acceptor probability and the second row
    is the donor probability. These probabilities corresponds to the
    middel <L NTs> NTs of the input seq.
    '''
    x = one_hot_encode(seq)[None, :, :].transpose(1, 2)  # shape: [1, 4, L]
    y = model(x)
    probs = torch.softmax(y, dim=1)  # shape: [1, 3, L]
    acceptor_probs = probs[0, :, 1]       # [L]
    donor_probs    = probs[0, :, 2]       # [L]
    return acceptor_probs.tolist(), donor_probs.tolist()


def run_spliceai_seq(seq, indices, threshold=0):
    # seq = 'N' * 5000 + seq + 'N' * 5000
    ref_seq_probs_temp = sai_predict_probs(seq, model)
    ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]
    acceptor_indices = {a: b for a, b in list(zip(indices, ref_seq_acceptor_probs)) if b >= threshold}
    donor_indices = {a: b for a, b in list(zip(indices, ref_seq_donor_probs)) if b >= threshold}
    return donor_indices, acceptor_indices