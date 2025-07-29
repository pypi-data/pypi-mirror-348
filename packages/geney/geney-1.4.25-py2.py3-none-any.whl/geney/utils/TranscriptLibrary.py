__all__ = ['TranscriptLibrary']

from .splicing_utils import adjoin_splicing_outcomes


class TranscriptLibrary:
    def __init__(self, reference_transcript, mutations):
        self.ref = reference_transcript.clone()
        self.event = reference_transcript.clone()
        self._transcripts = {'ref': self.ref, 'event': self.event}

        # Apply all mutations to 'event'
        for i, (pos, ref, alt) in enumerate(mutations):
            self.event.pre_mrna.apply_mutation(pos, ref, alt)
            if len(mutations) > 1:
                t = reference_transcript.clone()
                t.pre_mrna.apply_mutation(pos, ref, alt)
                self._transcripts[f'mut{i+1}'] = t
                setattr(self, f'mut{i+1}', t)

        # Make 'ref' and 'event' accessible as attributes too
        setattr(self, 'ref', self.ref)
        setattr(self, 'event', self.event)

    def predict_splicing(self, pos, engine='spliceai', inplace=False):
        self.splicing_predictions = {
            k: t.pre_mrna.predict_splicing(pos, engine=engine, inplace=True)
            for k, t in self._transcripts.items()
        }
        self.splicing_results = adjoin_splicing_outcomes(
            {k: t.pre_mrna.predicted_splicing for k, t in self._transcripts.items()},
            self.ref
        )
        if inplace:
            return self
        else:
            return self.splicing_results

    def get_event_columns(self, event_name, sites=('donors', 'acceptors')):
        """
        Extracts selected columns from splicing_results for a given event name
        (e.g., 'event', 'mut1', etc.)
        """
        metrics = (f'{event_name}_prob', 'ref_prob', 'annotated')
        if not hasattr(self, 'splicing_results'):
            raise ValueError("You must run predict_splicing() first.")

        cols = [(site, metric) for site in sites for metric in metrics]
        return self.splicing_results.loc[:, cols]

    def __getitem__(self, key):
        return self._transcripts[key]

    def __iter__(self):
        return iter(self._transcripts.items())
