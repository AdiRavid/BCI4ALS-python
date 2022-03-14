from ..paradigm.paradigm import Paradigm
from ..config.config import Config
from ..recorder.recorder import Recorder

from time import sleep
import numpy as np

class MIParadigm(Paradigm):
    """
    Paradigm subclass for the motor-imagery paradigm.
    """

    def __init__(self, config: Config):
        super(MIParadigm, self).__init__(config)
        self.num_trials = config.NUM_TRIALS
        self.CLASSES = config.CLASSES

    def start(self, recorder: Recorder):
        events = np.random.choice(list(self.CLASSES.keys()),
                                  size=self.num_trials * len(self.CLASSES))
        for event in events:
            print(self.CLASSES[event])
            sleep(5)
            recorder.push_marker(event)
