
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import os
import sys
import tensorflow as tf
import numpy as np
from keras.models import load_model
from importlib import resources


# Force device selection
if tf.config.list_physical_devices('GPU'):
    device = '/GPU:0'
elif sys.platform == 'darwin' and tf.config.list_physical_devices('MPS'):
    device = '/device:GPU:0'  # MPS uses /device:GPU:0 in TF
else:
    device = '/CPU:0'

# Model loading paths
if sys.platform == 'darwin':
    model_filenames = [f"models/spliceai{i}.h5" for i in range(1, 6)]
    model_paths = [resources.files('spliceai').joinpath(f) for f in model_filenames]
else:
    model_paths = [f"/tamir2/nicolaslynn/home/miniconda3/lib/python3.10/site-packages/spliceai/models/spliceai{i}.h5"
                   for i in range(1, 6)]

# Load models onto correct device
with tf.device(device):
    sai_models = [load_model(str(f)) for f in model_paths]


print(f"SpliceAI loaded to {device}.")

def one_hot_encode(seq):

    map = np.asarray([[0, 0, 0, 0],
                      [1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    seq = seq.upper().replace('A', '\x01').replace('C', '\x02')
    seq = seq.replace('G', '\x03').replace('T', '\x04').replace('N', '\x00')

    return map[np.fromstring(seq, np.int8) % 5]


def sai_predict_probs(seq: str, models: list) -> list:
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
    y = np.mean([models[m].predict(x, verbose=0) for m in range(5)], axis=0)
    # return y[0, :, 1:].T
    y = y[0, :, 1:].T
    return y[0, :], y[1, :]


def run_spliceai_seq(seq, indices, threshold=0):
    # seq = 'N' * 5000 + seq + 'N' * 5000
    ref_seq_probs_temp = sai_predict_probs(seq, sai_models)
    ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]
    acceptor_indices = {a: b for a, b in list(zip(indices, ref_seq_acceptor_probs)) if b >= threshold}
    donor_indices = {a: b for a, b in list(zip(indices, ref_seq_donor_probs)) if b >= threshold}
    return donor_indices, acceptor_indices