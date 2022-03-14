import mne
from ..config.config import Config


class BaseClassifier:
    """
    Basic class for a classifier for session eeg data.
    API includes training, prediction and evaluation.
    """

    def __init__(self, config: Config):
        pass

    def fit(self, data=mne.Epochs):
        pass

    def predict(self, data: mne.Epochs):
        pass

    def evaluate(self, data: mne.Epochs):
        pass
