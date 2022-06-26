from ..paradigm.paradigm import Paradigm
from ..config.config import Config
from ..recorder.recorder import Recorder


class P300Paradaigm(Paradigm):
    """
    Paradigm subclass for the p300 paradigm.
    """

    def __init__(self, config: Config):
        super(P300Paradaigm, self).__init__(config)

    def get_events(self):
        raise NotImplementedError


