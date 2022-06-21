import numpy as np

from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.config.config import Config


class DummyClassifier(BaseClassifier):
    """
    Dummy classifier that returns random prediction.
    """
    def __init__(self, config: Config):
        super().__init__(config)

    def predict(self, data: np.ndarray):
        return np.random.choice(list(self._config.LABELS2MARKERS.values()), 1)
