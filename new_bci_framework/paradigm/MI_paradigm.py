from new_bci_framework.paradigm.paradigm import Paradigm
from new_bci_framework.config.config import Config
from new_bci_framework.ui.ui import UI
from new_bci_framework.recorder.recorder import Recorder

import numpy as np


class MIParadigm(Paradigm):
    """
    Paradigm subclass for the motor-imagery paradigm.
    """

    def __init__(self, config: Config, ui: UI):
        super(MIParadigm, self).__init__(config)
        self.ui = ui
        self.num_trials_per_class = config.NUM_TRIALS_PER_CLASS
        self.time_between_trials = Config.TIME_PER_TRIAL
        self.CLASSES = config.CLASSES

    def start(self, recorder: Recorder):
        events = np.hstack([np.full(self.num_trials_per_class, key) for key in self.CLASSES.keys()])
        np.random.default_rng().shuffle(events)
        self.ui.run(recorder, events)

