import numpy as np

from new_bci_framework.classifier.base_classifier import BaseClassifier
from new_bci_framework.config.config import Config


class DummyClassifier(BaseClassifier):
    def __init__(self, config: Config):
        super().__init__(config)

    def fit(self, data: np.ndarray):
        super().fit(data)

    def predict(self, data: np.ndarray):
        return np.random.choice(list(self._config.TRIAL_LABELS.values()), 1)