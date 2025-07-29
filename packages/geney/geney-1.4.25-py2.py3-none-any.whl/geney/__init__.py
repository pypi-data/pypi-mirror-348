import os
import json
from pathlib import Path

from .utils.Fasta_segment import Fasta_segment
from . import utils  # this will now load all modules in utils/

# ─────────────────────────────────────────────────────────────────────────────
# Configuration Loader
# ─────────────────────────────────────────────────────────────────────────────

def get_config():
    config_file = Path.home() / '.oncosplice_setup_1_2' / 'config.json'
    if config_file.exists():
        with open(config_file) as f:
            config_json = json.load(f)
        config_setup = {
            k: {k_in: Path(p_in) for k_in, p_in in v.items()}
            for k, v in config_json.items()
        }
        # Override or extend paths for hg38
        config_setup.setdefault('hg38', {}).update({
            'titer_path': Path('/tamir2/nicolaslynn/tools/titer'),
            'yoram_path': Path('/tamir2/yoramzar/Projects/Cancer_mut/Utils'),
            'splicing_db': Path('/tamir2/nicolaslynn/data/OncosplicePredictions/hg38/splicing'),
        })
    else:
        print("⚠️ OncoSplice config not found at expected location.")
        config_setup = {}

    return config_setup

# Load config once
config = get_config()

# ─────────────────────────────────────────────────────────────────────────────
# Constants and Example IDs
# ─────────────────────────────────────────────────────────────────────────────

mut_id = 'KRAS:12:25227343:G:T'
epistasis_id = 'KRAS:12:25227343:G:T|KRAS:12:25227344:A:T'

# ─────────────────────────────────────────────────────────────────────────────
# Public API: available_genes
# ─────────────────────────────────────────────────────────────────────────────

def available_genes(organism='hg38'):
    """Yield gene names found in the MRNA_PATH/protein_coding directory."""
    mrna_path = config.get(organism, {}).get('MRNA_PATH')
    if not mrna_path:
        raise ValueError(f"MRNA_PATH not found in config for organism '{organism}'")
    for file in os.listdir(mrna_path / 'protein_coding'):
        gene = file.split('_')[-1].removesuffix('.pkl')
        yield gene

