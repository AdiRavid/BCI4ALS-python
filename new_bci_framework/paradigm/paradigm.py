from new_bci_framework.config.config import Config


class Paradigm:
    """
    This class decides the experiment paradigm. It holds all the information regarding the
    types of stimulus, the number of classes, trials etc.
    Subclasses may represent different paradigms such as p300, MI, etc.
    """
    def __init__(self, config: Config):
        self.config = config

    def get_events(self):
        raise NotImplementedError

