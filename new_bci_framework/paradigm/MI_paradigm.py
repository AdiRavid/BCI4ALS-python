from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.config.config import Config

import numpy as np


class MIParadigm(Paradigm):
    """
    Paradigm subclass for the motor-imagery paradigm.
    """
    def __init__(self, config: Config):
        super(MIParadigm, self).__init__(config)
        self.trial_labels = config.LABELS2MARKERS
        self.num_trials_per_class = config.NUM_TRIALS_PER_CLASS

    def get_events(self):
        """
        Creates an array of events according to the Config object.
        :return: A numpy array of events.
        """
        events = np.hstack([np.full(self.num_trials_per_class, key) for key in self.trial_labels.keys()])
        np.random.default_rng().shuffle(events)
        return events


