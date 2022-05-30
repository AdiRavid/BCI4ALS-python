from ..recorder.recorder import Recorder
from ..config.config import Config
from ..classifier.base_classifier import BaseClassifier

from typing import Optional


class Paradigm:
    """
    This class decides the experiment paradigm. It holds all the information regarding the
    types of stimulus, the number of classes, trials etc.
    All the things that need to happen during the recording for this paradigm are under this classes
    responsibility (showing a ui, creating events, pushing markers to an active recording, etc.)
    Sublcasses may represent different paradigms such as p300, MI, etc.
    """

    def __init__(self, config: Config):
        self.config = config

    def get_events(self):
        raise NotImplementedError

