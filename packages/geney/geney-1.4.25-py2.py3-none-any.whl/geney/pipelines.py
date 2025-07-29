# Home of the frequently used pipelines that everyone needs
import pandas as pd
from datetime import datetime

from .Gene import Gene
from .utils.mutation_utils import MutationalEvent
from .SpliceSimulator import SpliceSimulator
from .Oncosplice import Oncosplice
from .utils.TranscriptLibrary import TranscriptLibrary


def max_splicing_delta(mut_id, transcript_id=None, splicing_engine='spliceai'):
    m = MutationalEvent(mut_id)
    assert m.compatible(), 'Mutations in event are incompatible'
    reference_transcript = Gene.from_file(
        m.gene).transcript(transcript_id).generate_pre_mrna().generate_mature_mrna().generate_protein()
    tl = TranscriptLibrary(reference_transcript, m)
    splicing_results = tl.predict_splicing(m.position, engine=splicing_engine, inplace=True).get_event_columns('event')
    ss = SpliceSimulator(splicing_results, tl.event, feature='event', max_distance=100_000_000)
    return ss.max_splicing_delta('event_prob')


def oncosplice_pipeline_single_transcript(mut_id, transcript_id=None, splicing_engine='spliceai', ):
    m = MutationalEvent(mut_id)
    assert m.compatible(), 'Mutations in event are incompatible'
    reference_transcript = Gene.from_file(
        m.gene).transcript(transcript_id).generate_pre_mrna().generate_mature_mrna().generate_protein()
    tl = TranscriptLibrary(reference_transcript, m)
    splicing_results = tl.predict_splicing(m.position, engine=splicing_engine, inplace=True).get_event_columns('event')
    ss = SpliceSimulator(splicing_results, tl.event, feature='event', max_distance=100_000_000)

    base_report = pd.Series({'mut_id': mut_id,
                             'gene': m.gene,
                             'transcript_id': reference_transcript.transcript_id,
                             'primary_transcript': reference_transcript.primary_transcript,
                             'splicing_engine': splicing_engine,
                             'time_of_execution': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    ss_metadata = ss.report(m.positions[0])
    report = []
    for variant_transcript, isoform_metadata in ss.get_viable_transcripts(metadata=True):
        onco = Oncosplice(reference_transcript.protein, variant_transcript.protein, reference_transcript.cons_vector)
        report.append(pd.concat([base_report, ss_metadata, isoform_metadata, onco.get_analysis_series()]))
    return pd.DataFrame(report)


def oncosplice_pipeline_all_transcripts(mut_id, splicing_engine='spliceai'):
    m = MutationalEvent(mut_id)
    assert m.compatible(), 'Mutations in event are incompatible'
    reports = []
    for transcript_id in Gene.from_file(m.gene).transcripts.keys():
        reports.append(oncosplice_pipeline_single_transcript(mut_id, transcript_id, splicing_engine=splicing_engine))
    return pd.concat(reports, axis=1)


def get_tcga_annotations(mut_ids):
    pass



def generate_epitopes():
    pass




