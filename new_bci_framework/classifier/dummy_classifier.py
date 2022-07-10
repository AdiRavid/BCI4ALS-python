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
        """
        preforms the prediction on the given data
        :param data: data to predict on
        :return: classification for the data
        """
        return np.random.choice(list(self._config.LABELS2MARKERS.values()), 1)

    def load_classifier(self):
        pass
