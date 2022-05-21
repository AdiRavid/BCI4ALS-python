import numpy as np

from new_bci_framework.config.config import Config


class BaseClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        self._config = config


    def fit(self, data: np.ndarray):
        pass

    def predict(self, data: np.ndarray):
        pass