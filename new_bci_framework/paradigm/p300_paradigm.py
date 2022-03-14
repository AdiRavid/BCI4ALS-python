from ..paradigm.paradigm import Paradigm
from ..config.config import Config
from ..recorder.recorder import Recorder


class P300Paradaigm(Paradigm):
    """
    Paradigm subclass for the p300 paradigm.
    """

    def __init__(self, config: Config):
        super(P300Paradaigm, self).__init__(config)

    def start(self, recorder: Recorder):
        pass
        # start a trial
        recorder.push_marker("this trial's marker")

