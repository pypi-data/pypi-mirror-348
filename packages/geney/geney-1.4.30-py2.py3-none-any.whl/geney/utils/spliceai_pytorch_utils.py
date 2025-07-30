
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import sys
import numpy as np


import torch
from spliceai_pytorch import SpliceAI
model = SpliceAI.from_preconfigured('10k')


if sys.platform == 'darwin':
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

if sys.platform == 'linux':
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


print(f"SpliceAI loaded to {device}.")
model.to(device)

def one_hot_encode(seq):

    map = np.asarray([[0, 0, 0, 0],
                      [1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    seq = seq.upper().replace('A', '\x01').replace('C', '\x02')
    seq = seq.replace('G', '\x03').replace('T', '\x04').replace('N', '\x00')

    return map[np.fromstring(seq, np.int8) % 5]


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
    x = one_hot_encode(seq)[None, :]
    y = model(x)
    y = y[0, :, 1:].T
    return y[0, :], y[1, :]


def run_spliceai_seq(seq, indices, threshold=0):
    # seq = 'N' * 5000 + seq + 'N' * 5000
    ref_seq_probs_temp = sai_predict_probs(seq, model)
    ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]
    acceptor_indices = {a: b for a, b in list(zip(indices, ref_seq_acceptor_probs)) if b >= threshold}
    donor_indices = {a: b for a, b in list(zip(indices, ref_seq_donor_probs)) if b >= threshold}
    return donor_indices, acceptor_indices