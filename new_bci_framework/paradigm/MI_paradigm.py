from ..paradigm.paradigm import Paradigm
from ..config.config import Config
from ..recorder.recorder import Recorder

from time import sleep
import numpy as np
from nptyping import NDArray

class MIParadigm(Paradigm):
    """
    Paradigm subclass for the motor-imagery paradigm.
    """

    def __init__(self, config: Config):
        super(MIParadigm, self).__init__(config)
        self.num_trials_per_class = config.NUM_TRIALS_PER_CLASS
        self.time_between_trials = Config.TIME_PER_TRIAL
        self.CLASSES = config.CLASSES
        self.events = np.hstack([np.full((self.num_trials_per_class), key)
                                 for key in self.CLASSES.keys()])
        np.random.default_rng().shuffle(self.events)

    def start(self, recorder: Recorder):
        for event in self.events:
            recorder.push_marker(event)
            sleep(self.time_between_trials)

    def get_events(self) -> NDArray:
        return self.events
